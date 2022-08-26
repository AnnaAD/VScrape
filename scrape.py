import requests
import json
import csv

url = "https://api.benchsci.com/v1/reagents/_search"
keys = ['application_stats', 'published_figures_count']

output = []
keys_of_interest = []
with open('genes.txt') as f:
    auth_token = f.readline().strip()
    genes = f.readlines()

genes = [g.strip() for g in genes]

print("auth token", auth_token)
print("gene list", genes)
for gene in genes:
    print("loading", gene)
    try:
        working = {"name": gene}
        payload="{\"match_criteria\":\"REAGENTS\",\"pagination\":{\"offset\":0,\"limit\":20},\"sort\":{\"method\":\"TOTAL_FIGURES\",\"order\":\"DESC\"},\"should\":[{\"reagent_proteins_gene_and_aliases\":{\"must\":[\""+gene+"\"]}}],\"stats\":{\"count_all_records\":true}}"
        headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text)["results"]

        working["figures_count"] = data[0]["figures_count"]
        working["url"] = data[0]["reagent_specs"]["url"]
        working["catalog_nb"] = data[0]["catalog_nb"]
        working["supplier"] = data[0]["reagent_specs"]["supplier"]
        
        for app in data[0]["application_stats"]:
            if(app["application"] == "Immunohistochemistry"):
                working["ihc"] = True
        
        if("ihc" not in working):
            working["ihc"] = False
    
        output.append(working)
    except:
        print("failed to load", gene)

with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = output[0].keys())
    writer.writeheader()
    writer.writerows(output)

print(output)
