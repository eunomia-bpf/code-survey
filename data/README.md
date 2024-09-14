# The data will be generated here.

How to use the dataset:

## The feature version data set

Without add llm survey result:

- See [feature_commit_details.csv](feature_commit_details.csv)

With llm survey result:

- See [feature_commit_details_survey.csv](feature_commit_details_survey.csv)

Feature versions is tagged by human and rechieved from the following source:

- https://github.com/isovalent/ebpf-docs/blob/master/data/feature-versions.yaml

How to get the newest feature version data:

```bash
# get the newest feature version data
wget https://raw.githubusercontent.com/isovalent/ebpf-docs/master/data/feature-versions.yaml -O data/feature-versions.yaml
# generate the feature version data with commit details
python3 data/gen_feature_csv.py
# run the survey with llm
python3 surver/survey.py survey/feature_survey.yml data/feature_commit_details.csv data/feature_commit_details_survey.csv
```

## The commit data set

```
# get the commit csv

```
