if grep "MDRS answer/log status: 'OK'" $1 > /dev/null
then
	echo "OK"
else
	echo "NOK"
fi
