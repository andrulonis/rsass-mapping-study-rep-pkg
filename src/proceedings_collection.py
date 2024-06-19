from lxml import etree
import csv
from tqdm import tqdm
import sys
import os
from zipfile import ZipFile 
from zipfile import ZIP_DEFLATED

DBLP_XML = 'data/dblp-2024-06-02.xml'
DBLP_XML_ZIP = 'data/dblp-2024-06-02.zip'

DBLP_DTD = 'data/dblp-2023-06-28.dtd'
# DBLP_DTD = 'data/dblp-new.dtd'

YEAR_MIN = 2012
YEAR_MAX = 2024

SEAMS_FIX = True
#I included the second / because otherwise if there is a conference e.g. icrac it will get included.
SA_VENUES = tuple([
    'conf/icsa/',
    'conf/ecsa/',
    'conf/wicsa/',
    'conf/qosa/',
    'conf/cbse/',
    'journals/jsa/'
])

RO_VENUES = tuple([
    'conf/icra/', 
    'conf/iros/',
    'conf/rss/',
    'conf/irc/',
    'journals/trob/',
    'journals/ral/',
    'journals/ijrr/',
    'journals/scirobotics/'
])

SAS_VENUES = tuple([
    'conf/acsos/',
    'conf/saso/',
    'conf/icac/',
    'conf/seams/',
    'journals/taas/'
])

venue_to_category = {
    SA_VENUES : "Software_Architecture",
    RO_VENUES : "Robotics",
    SAS_VENUES : "Self-Adaptive_Systems"
}

ARCHITECTURE_KWORDS = ["architect"]
ROBOTICS_KWORDS = ["robot"]
SAS_KWORDS = ["self-", "adapt", "reconfig"]

FROM_ROBOTICS = ARCHITECTURE_KWORDS + SAS_KWORDS
FROM_SOFTWARE = ROBOTICS_KWORDS + SAS_KWORDS
FROM_SAS = ROBOTICS_KWORDS + ARCHITECTURE_KWORDS

venue_to_words = {
    SA_VENUES : FROM_SOFTWARE,
    RO_VENUES : FROM_ROBOTICS,
    SAS_VENUES : FROM_SAS
}

filter_by_title = True
out_csv_title = "data/all"


# Iterate over a large-sized xml file without the need to store it in memory in
# full. Yields every next element. Source:
# https://stackoverflow.com/questions/9856163/using-lxml-and-iterparse-to-parse-a-big-1gb-xml-file
def iterate_xml(xmlfile):
    etree.DTD(file=DBLP_DTD)
    doc = etree.iterparse(xmlfile, events=('start', 'end'), load_dtd=True, resolve_entities=True, encoding='utf-8')
    _, root = next(doc)
    start_tag = None
    for event, element in tqdm(doc):
        if event == 'start' and start_tag is None:
            start_tag = element.tag
        if event == 'end' and element.tag == start_tag:
            yield element
            start_tag = None
            root.clear()

def title_criteria(key, venue_list, title, counter, explain=False, dblp_entry=None): 
    title_lowered = title.lower()
    title_keywords = venue_to_words[venue_list]
    category = ""
    if explain:
        print("keywords " + str(title_keywords) + "found in " + str(title) + "is " + str(any(keyword in title for keyword in title_keywords)))
        print("key starts with " + str(venue_list) + "in " + str(key) + "is " + str(key.startswith(venue_list)))
    
    return_value = ((key.startswith(venue_list) or (SEAMS_FIX and key.startswith("conf/icse") and (dblp_entry is not None) and ("SEAMS" in dblp_entry.find('booktitle').text)) ) and any(keyword in title_lowered for keyword in title_keywords))
    if(return_value): 
        counter[0]+=1
        category =  venue_to_category[venue_list]
    return category

def venue_criteria(key, venue_list, counter, explain=False, dblp_entry=None): 
    category = ""
    if explain:
        print("key starts with " + str(venue_list) + "in " + str(key) + "is " + str(key.startswith(venue_list)))
    

    old_seams_check = (SEAMS_FIX) and key.startswith("conf/icse") and (dblp_entry is not None) and ("SEAMS" in dblp_entry.find('booktitle').text)
    return_value = ( (key.startswith(venue_list) or (old_seams_check)) )
    if(return_value): 
        counter[0]+=1
        category =  venue_to_category[venue_list]
    return category


def append_joser(csv_writer):
    #Since the JOSER journal is not in DBLP (as of yet), we manually add its already title-filtered entries to the final csv.
    print("Adding entries from JOSER manually...")
    
    with open("data/joser_filtered.csv", 'r', encoding='utf-8', newline="") as csvfile:
        venue_reader = csv.reader(csvfile)
        next(venue_reader) #skip header

        for joser_row in venue_reader:
            csv_writer.writerow(joser_row)
            

def parse_entries():
    HITS = 0

    csv_file = open(out_csv_title + ".csv", 'w', encoding='utf-8', newline="")
    writer = csv.writer(csv_file, delimiter=",")
    header = ["hit num", "title", 'year', "authors", "key", "ee", "venue_category"]
    writer.writerow(header)




    # The db key should start with any of the venues we are interested in,
    # as well as be within the desired year range.
    ro_counter = [0]
    sa_counter = [0]
    sas_counter = [0]
    for dblp_entry in iterate_xml(DBLP_XML):
        key = dblp_entry.get('key')
        year_subelem = dblp_entry.find('year')

        if((year_subelem is not None) and (int(year_subelem.text) >= YEAR_MIN) and (int(year_subelem.text) <= YEAR_MAX)):
            # Remove any potential HTML content (such as <i>) from the title.
            title = ''.join(dblp_entry.find('title').itertext())


            if(filter_by_title):
                match_robotics = title_criteria(key,RO_VENUES, title, ro_counter)
                match_software = title_criteria(key,SA_VENUES, title, sa_counter)
                match_adaptive = title_criteria(key, SAS_VENUES, title, sas_counter, dblp_entry=dblp_entry)
            else:
                match_robotics = venue_criteria(key,RO_VENUES, ro_counter)
                match_software = venue_criteria(key,SA_VENUES, sa_counter)
                match_adaptive = venue_criteria(key, SAS_VENUES, sas_counter, dblp_entry=dblp_entry)

            matched_criteria = match_robotics or match_software or match_adaptive
            if(matched_criteria): #an any with extra steps to get the return value in a variable.
                # add to result.
                # Merge the names of all authors of the work.
                authors = ' & '.join(''.join(author.itertext()) for author in
                    dblp_entry.findall('author'))

                # Obtain the source (usually in the form of a DOI link).
                ee = dblp_entry.find('ee')
                if ee is not None:
                    ee = ee.text

                # Compile csv row.
                row = [HITS,
                        title.replace(',', ';'),
                        dblp_entry.find('year').text,
                        authors,
                        key,
                        ee,
                        matched_criteria]

                writer.writerow(row)

                HITS+=1
    if SEAMS_FIX:
        append_joser(writer)
    # Parse all entries in the DBLP database.
    print("TOTAL HITS : " + str(HITS) + " ROBOTICS HITS: " + str(ro_counter[0]) + " ARCHITECTURE HITS: " + str(sa_counter[0]) + " SAS HITS: " + str(sas_counter[0]), end="")
    print("")

def extract_dblp():
    if(os.path.exists(DBLP_XML)):
        print("Loading existing dblp xml file...")
        return
    elif(os.path.exists(DBLP_XML_ZIP)):
        print("Unzipping existing dblp zip file (this should only happen the first time)...")

        with ZipFile(DBLP_XML_ZIP, 'r', compression=ZIP_DEFLATED, allowZip64=True) as zObject: 
            zObject.extractall( 
                path="data/") 
            return
    else:
        raise Exception("For some reason, neither the xml or zip version of the dblp database could be found")




if __name__ == "__main__":
    
    extract_dblp()
    try:
        passed_options = sys.argv[1:]
    except IndexError:
        passed_options = [] #probably superfluous

    
    if("--all" in passed_options):
        filter_by_title = False
        print("Collecting all studies for each venue's proceedings")
    elif("--pilot" in passed_options):
        print("Collecting the studies, but not accounting for SEAMS patch, which is the version used for the two pilots.")
        #for the pilot, we had not yet discovered the absence of SEAMS papers due to their cataloging under conf/icse. 
        SEAMS_FIX = False
        out_csv_title+="_pilot"


    elif(filter_by_title == True):
        print("Collecting and doing title keyword filtering, use option '--all' to turn off title filtering")
        out_csv_title+="_filtered_by_title"
    parse_entries()
 



