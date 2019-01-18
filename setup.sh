#  add confirmation and explanation of actions here
echo
echo "This will install dependenceis for microslack.  Do you wish to continue? [y/n]"
read reply
echo    # (optional) move to a new line
if [[ $reply != "y" ]]
then
  echo "Aborted microslack dependency install..."
  echo
  exit 1
fi

echo "Installing microslack python dependencies via pip..."
echo
echo "Running: sudo pip install argparse"
echo
sudo pip install argparse
echo
echo " **argparse installed via pip**"
echo
echo "Running: sudo pip install slackclient"
echo
sudo pip install slackclient
echo
echo " **slackclient installed via pip**"
echo
echo "Install script run for microslack python dependencies via pip. Check prior console output to confirm successful install."
