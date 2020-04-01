# installing tor

``` bash
sudo apt update
sudo apt install apt-transport-https
sudo add-apt-repository universe
wget -q -O - https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | sudo apt-key add -
echo "deb https://deb.torproject.org/torproject.org $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list
sudo apt update
sudo apt install tor deb.torproject.org-keyring torbrowser-launcher
sudo apt install tor

service tor stop

echo HashedControlPassword $(tor --hash-password "123" | tail -n 1) >> /etc/tor/torrc
echo "ControlPort 9051" >> /etc/tor/torrc

service tor start

echo -e 'AUTHENTICATE "123"' | nc 127.0.0.1 9051
```

