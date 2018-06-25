#  add confirmation and explanation of actions here
echo "\n"
echo "Installing microslack python dependencies via pip...\n"

echo "Running: sudo pip install argparse\n"
sudo pip3 install argparse
echo "\n"
echo " **argparse installed via pip**\n"

echo "Running: sudo pip install slackclient\n"
sudo pip3 install slackclient
echo "\n"
echo " **slackclient installed via pip**\n"

echo "Install script run for microslack python dependencies via pip. Check console output above to confirm successful install.\n"
