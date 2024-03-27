# How is software architecture-based self-adaptation applied in robotics?
This repository is a companion page for the following (pending) publication:
> Author Names. Publication year. Thesis / Paper title. Publication venue / proceedings.

It contains all the material required for replicating the study, including: X, Y, and Z.

## How to cite us
The scientific article describing design, execution, and main results of this study is available [here](https://www.google.com).<br> 
If this study is helping your research, consider to cite it is as follows, thanks!

```
@article{,
  title={},
  author={},
  journal={},
  volume={},
  pages={},
  year={},
  publisher={}
}
```

## Quick start
Here a documentation on how to use the replication material should be provided.


### Getting started
0. If you are not interested in any of the details, and would simply like to reproduce everything (including safely installing dependencies), we provide a shell script to do so, simply run `./everything.sh`, on a unix-based system. For your convenience, if you are using Windows we provide an `everything.bat` script to run instead. For either version, you only need to pass the keyword which refers to python3 on your system as an argument, so either `--python3` if you use python 3 by typing `python3` or `--python` if you use `python` to use python 3. 

1. This reproduction package relies (only) on Python. Please see that you have Python 3 installed on your system. Then, you can choose to create a virtual environment, or simply run  `pip install -r requirements.txt` in the root folder of this repository after you have cloned it. We are unaware of any version conflicts, and presume most installable versions of each python dependency should work.



2. The reproduction package includes the exact snapshot of dblp used for the study. Unfortunately, this snapshot is no longer hosted by dblp, making this the one of the few places it likely exists. Due to its large size we have compressed it to a zip file, however, on running our scripts it should extract itself. The reproduction package revolves around three scripts: proceedings_collection.py, pilots_and_final.py, and generate_plots.py. Every script can be run by opening a terminal in the root of the repository and typing some form of `python script_name.py`, for example `python proceedings_collection.py`. Keep in mind on some system you may have to specify python3, so `python3 script_name.py`.

3. Here we will cover proceedings_collection.py. This script parses the XML of the dblp snapshot, and collected potentially-relevant studies in accordance with the procedure and time criteria outlined in our study. There are two arguments/options that can be passed to the script `--all` and `--pilot`. The first option, `--all` means we collect every single study without filtering by their titles. This allows the user to try different keywords manually to determine how many studies this may result in, and aids in the transparency of the filtering process. By default, the title keyword filtering is applied if the `--all` option is not specified. The second option `--pilot` produces the .csv of potentially-relevant as it was used for the pilot studies. This distinction exists as between the pilot studies and the final selection we uncovered that the proceedings of some years of the SEAMS conference which we target, are misleadingly categorized under the ICSE conference (with which it is co-located) which we do not target. We remedied this after the pilot, meaning the seeded randomized extraction of potentially-relevant studies was no longer reproducible without maintaining these two distinct versions.

4. For pilots_and_final.py to be able to use this script fully, it requires having run the proceedings_collection.py script with the `--pilot` option prior. This, as the pilot section of this script relies on a different version of the potentially-relevant studies as outlined in step 3. Unfortunately, this also impacts the final selection csv file, as we create this based on removing those studies used in the two pilots.

5. For generate_plots.py this script generates a bar plot for every data parameter from the vertical analysis. This will generate all those found in our paper, but also those we did not include but use to report on the results. There is one option which can be passed to this script `--show` this makes it so that the plots are displayed to the user one by one rather than saved in a folder called plots. This is useful if you are modifying the script and would not like to overwrite previous versions of the plots.

### Snowballing
The snowballing was done semi-manually. For forward snowballing we used Google Scholar to find all the papers which cite ours, manually recording the DOI and title of each study and removing duplicates.
For the backwards snowballing, we made use of https://github.com/helenocampos/PDFReferencesExtractor, and corrected any mistakes, and used tools such as Zotero to grab the missing DOIs from titles when this occurred. 

## Repository Structure
This is the root directory of the repository. The directory is structured as follows:

    template-replication-package
     .
     |
     |--- src/                             Source code used in the thesis / paper
     |
     |--- data/                            Data necessary to run the various scripts.
     |              
  


<!-- ## Replication package naming convention
The final name of this repository, as appearing in the published article, should be formatted according to the following naming convention:
`<short conference/journal name>-<yyyy>-<semantic word>-<semantic word>-rep-pkg`

For example, the repository of a research published at the International conference on ICT for Sustainability (ICT4S) in 2022, which investigates cloud tactics would be named `ICT4S-2022-cloud-tactics-rep-pkg` -->
