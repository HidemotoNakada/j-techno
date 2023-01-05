jupyter nbconvert '--Exporter.preprocessors=["regexremove.MyRegexRemovePreprocessor"]' \
 --MyRegexRemovePreprocessor.input="['^# hide']"\
  ../parts/k-means.ipynb