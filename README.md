Hello
=====

Thanks for taking the time to complete this code test, we really appreciate it!

Introduction
----

Welcome to the bunnies API! Bunnies live in rabbit holes, and as a user you can manage rabbit holes and the bunnies that live in them. We also love to capture analytics about our users so we do some basic tracking too.


Instructions:
----

This repository contains a simple Django Rest Framework API project with a couple of apps and models. We've added some
basic views and tests. Essentially we'd like you to fix the project so that the whole test suite passes.

Please _clone_ (don't fork) this repository, complete the test and then upload to a public repository on github and send us the link. The instructions below are for use with pipenv, but of course you can setup the 
project however is most comfortable for you ( virtualenv / docker etc. ). Regardless, you'll need python3.6+ to run this code.

```bash
git clone git@github.com:crowdcomms/crowdcomms-django-test.git
cd crowdcomms-django-test
git remote remove origin
git remote add origin <Your Repository>
pipenv shell
pipenv install
python manage.py test
```

You should see a list of failing test cases, please examine and modify the code base to make these pass.

Please don't spend more than 2 hours on this task (not including initial download and setup). If you reach 2 hours, please commit your code as-is and supply a pull request.

