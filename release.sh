#!/usr/bin/env bash
PROJECT_NAME="suapintegration"
FULL_IMAGE_NAME="ifrn/$PROJECT_NAME"
ROOT_DIR=$( pwd )


if [ $# -eq 0 ]; then
  echo ''
  echo 'NAME '
  echo '       release'
  echo 'SYNOPSIS'
  echo '       ./release.sh [-l|-g|-p|-a] <version>'
  echo 'DESCRIPTION'
  echo '       Create a new release $PROJECT_NAME image.'
  echo 'OPTIONS'
  echo '       -l         Build only locally'
  echo '       -g         Push to Github'
  echo '       -p         Registry on PyPi'
  echo '       -a         Push and registry on Github'
  echo '       <version>  Release version number'
  echo 'EXAMPLES'
  echo '       o   Build a image to local usage only:'
  echo '                  ./release.sh -l 1.0'
  echo '       o   Build and push to GitHub:'
  echo '                  ./release.sh -g 1.0'
  echo '       o   Build and registry on PyPi:'
  echo '                  ./release.sh -p 1.0'
  echo '       o   Build, push to Guthub and registry on PyPi:'
  echo '                  ./release.sh -a 1.0'
  echo "LAST TAG: $(git tag | tail -1 )"
  exit
fi

OPTION=$1
VERSION=$2

create_setup_cfg_file() {
  printf "\n\nCREATE setup.cfg file\n"
  sed "s/lib_version/$VERSION/g" $ROOT_DIR/setup.pytemplate > $ROOT_DIR/setup.py 
}

lint_project() {
  printf "\n\nLINT project $PROJECT_NAME $VERSION\n"
  docker run --rm -it  -v `pwd`:/src kelsoncm/release_to_pypi sh -c 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 . --count --max-complexity=10 --max-line-length=127 --statistics'
}


build_project() {
  printf "\n\nBUILD project $PROJECT_NAME $VERSION\n"
  docker run --rm -it  -v `pwd`:/src kelsoncm/release_to_pypi sh -c "python setup.py sdist && chmod -R 777 dist && chmod -R 777 $PROJECT_NAME.egg-info"
}


push_to_github() {
  if [[ "$OPTION" == "-g" || "$OPTION" == "-a" ]]
  then
    printf "\n\n\GITHUB: Pushing\n"
    git add setup.py \
    && git commit -m "Release $PROJECT_NAME $VERSION" \
    && git tag $VERSION \
    && git push --tags origin master
  fi
}

send_to_pypi() {
  if [[ "$OPTION" == "-p" || "$OPTION" == "-a" ]]
  then
    printf "\n\n\PYPI: Uploading\n"
    docker run --rm -it -v `pwd`:/src kelsoncm/release_to_pypi twine upload dist/$PROJECT_NAME-$VERSION.tar.gz
  fi
}

create_setup_cfg_file \
&& lint_project \
&& build_project \
&& push_to_github \
&& send_to_pypi

echo ""
echo "Done."
