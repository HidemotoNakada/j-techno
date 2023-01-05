jupyter nbconvert '--Exporter.preprocessors=["regexremove.MyRegexRemovePreprocessor"]' \
 --MyRegexRemovePreprocessor.input="['^# hideinput']"\
 --MyRegexRemovePreprocessor.output="['^# hideoutput']"\
 --MyRegexRemovePreprocessor.all="['^# hideall']"\
  ../parts/k-means.ipynb