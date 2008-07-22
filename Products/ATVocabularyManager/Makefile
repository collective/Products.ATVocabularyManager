PRODUCT_NAME = ATVocabularyManager

test:
	@if [ $(INSTANCE_HOME) ]; then\
       $(INSTANCE_HOME)/bin/zopectl test --package=Products.$(PRODUCT_NAME) --test-file-pattern=$(TEST) ;\
       echo "You may specify a certain test-module using make TEST=testModuleName";\
    else\
       echo "please set 'INSTANCE_HOME'!";\
	fi

## removes compiled python and backup files
clean:
	@find . -name "*.pyc" -exec rm {} \;
	@find . -name "*~" -exec rm {} \;