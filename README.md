# n2c
### Map U.S. Food and Drug Administration (FDA) National Drug Codes (NDC) to Drug Classes  
###### codename: n2c
*_Mapping NDCs to Anatomical Therapeutic Chemical (ATC) Level 4_*

**This script is a newer version of https://github.com/fabkury/ndc_map . Please use this one and not ndc_map.**
  
This script provides the ATC classes of each FDA National Drug Code (NDC) in an input file. The input file is a simple text list with one NDC per line. The script works by querying the online RxNorm API at https://rxnav.nlm.nih.gov/.  
  
This script is just a helper to query the API in bulk and write the resposes to a convenient CSV file. The mappings themselves are maintained and provided for free by RxNorm.  
    
This work is an update from what was presented as a poster at the 2017 Annual Symposium of the American Medical Informatics Association (AMIA). I have also published a deeper analysis and comparison of drug classification systems in a paper (_Desiderata for Drug Classification Systems for their Use in Analyzing Large Drug Prescription Datasets_ -- https://github.com/fabkury/ddcs/blob/master/2016-dmmi-fk.pdf). **_TL;DR_**: unless your use case is particularly specific, ATC is the best drug classification for most cases of large dataset analyses. The Veterans' Affairs Drug Classes attain the same high level of coverage of NDCs as ATC, but they don't provide a comprehensive and accessible hierarchy like ATC.  

### How to run
1) Make sure you have Python installed. This is a Python script.
2) Create a flat text file with one NDC per line. E.g. *input_ndc_list.txt*.
3) Run:

```python
python n2c.py input_ndc_list.txt
```
4) Wait for the script to complete. If you want to interrupt, press **P**. *The script caches its queries. If it is interrupted, it resumes from where it left off. You don't need to complete it all in one go.*     
  
### Contact the author
Please feel free to contact me about this work! Reading and using someone else's code can become so much easier after a quick conversation.  
Contact me at 191206@kury.dev. **_--Fabrício Kury_**  
  
Search tags: thesaurus drug class map equivalence correspondence classification
  
