		# Webvalley Factoid address: FA3bNrrt7F34ANPDnRdQESRhN3SD3MQJqUZWdpbKGX2J66wxBFbP
		# Webvalley Entry Credit address: EC1rV8ZrsscKmTA2K4CX3xQRPki2FM18E79MRoJuiAq9g4yGoFhB
		# ChainID: a4ab1e2ef212208b3513c5f06fcdcfa79b7c2b610526ce2dc374bb789700a791
		# Entryhash: b18b4b1c70880211b9c3580b08a6ac0e3041804c5bd7fe7c46605798242a93c1

# DO NOT RUN THIS AS ROOT

# confirmed working on ubuntu 16.04 as of june 2017	
# note: factomd does a lot of disk access. ssd strongly recommended.

# download the blockchain and factom system (urls may change! check docs.factom.com for the latest links.)
wget http://www.factom.com/assets/site/factom_bootstrap.zip
wget https://github.com/factomproject/distribution/releases/download/v0.4.2.3/factom-amd64.deb

# unzip the blockchain and install the factom system
sudo apt-get install -y unzip
unzip *.zip
sudo apt-get update
sudo dpkg -i *.deb
sudo apt-get install -f

#
In three seperate terminals:
factomd
factom-walletd
factom-cli

factomd takes a while to sync
can open port 8090 to view progress on http

generate addresses with 
factom-cli newfctaddress > fctaddress
factom-cli newecaddress > ecaddress

then buy some ec with
factom-cli buyec FA3bNrrt7F34ANPDnRdQESRhN3SD3MQJqUZWdpbKGX2J66wxBFbP EC1rV8ZrsscKmTA2K4CX3xQRPki2FM18E79MRoJuiAq9g4yGoFhB 50

Last one is used to do stuff. 	



