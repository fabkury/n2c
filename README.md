# n2c
### Map U.S. Food and Drug Administration (FDA) National Drug Codes (NDC) to Drug Classes  
###### codename: n2c
*_Mapping NDCs to Anatomical Therapeutic Chemical (ATC) Level 4_*

## **This script is a newer version of https://github.com/fabkury/ndc_map . Please use this one and not ndc_map. ndc_map is deprecated and might not work if you try. This script does not have all features of ndc_map, but it will be the one receiving updates moving forward.**
  
This script provides the ATC classes of each FDA National Drug Code (NDC) in an input file. The input file is a simple text list with one NDC per line. The script works by querying the online RxNorm API at https://rxnav.nlm.nih.gov/.  
  
This script is just a helper to query the API in bulk and write the resposes to a convenient CSV file. The mappings themselves are maintained and provided for free by RxNorm.  
    
This work is an update from what was presented as a poster at the 2017 Annual Symposium of the American Medical Informatics Association (AMIA). I have also published a deeper analysis and comparison of drug classification systems in a paper (_Desiderata for Drug Classification Systems for their Use in Analyzing Large Drug Prescription Datasets_ -- https://github.com/fabkury/ddcs/blob/master/2016-dmmi-fk.pdf). **_TL;DR_**: unless your use case is particularly specific, ATC is the best drug classification for most cases of large dataset analyses. The Veterans' Affairs Drug Classes attain the same high level of coverage of NDCs as ATC, but they don't provide a comprehensive and accessible hierarchy like ATC.  

### A) How to run
1) Make sure you have Python installed. This is a Python script.
2) Create a flat text file with one NDC per line. E.g. *input_ndc_list.txt*.
3) Run:

```python
python n2c.py input_ndc_list.txt
```
4) Wait for the script to complete. The script will create a CSV file with the NDCs and their ATC-4 classes (if any).
 - If you want to interrupt, press **P**.
 - You don't need to complete it all in one go. The script caches its queries. If it is interrupted, it resumes from where it left off.  
  
### B) But I just need a simple file with NDCs and their ATC classes! I don't know Python!
- Download file *package_NDC_ATC_classes.csv*. It contains the FDA NDC Directory (https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory) as of July 22, 2024, mapped to ATC-4 classes.
- 76.1% of all NDCs in the FDA NDC directory were successfully mapped to at least 1 ATC-4 class. Remember that one NDC may be mapped to more than one class.
- The FDA Directory does not contain all NDCs that have ever existed.  
    
### C) Contact the author
**C.1)** If you can send me your list of NDCs, I can run this script for you. Many people have approached me in the past with this request.  
**C.2)** Please feel free to contact me about this work! Reading and using someone else's code can become so much easier after a quick conversation.  
  
Contact me at 191206@kury.dev. **_-- Fabrício Kury_**  
  
Search tags: thesaurus drug class map equivalence correspondence classification
  
