
export var webscore_examples = {


	get_py: (url) => {
		return `
import requests

url = '${url}'

payload = {
    'input': 'Bart Simpson',
    'filter_input': 0,
    'use_proxy': 1,
    'collected_data': 1
}

response = requests.get(url, params=payload)
print(response.json())`
},


	get_bash: (url) => {
		return `
curl -G "${url}" \\
--data-urlencode "input=bart simpson" \\
--data-urlencode "filter_input=0" \\
--data-urlencode "use_proxy=1" \\
--data-urlencode "collected_data=1"`
	},


	get_js: (url) => {
		return `
import axios from "axios"

const options = {
	url: '${url}',
	method: 'GET',
	data: {
		input: "bart simpson",
		filter_input: 1,
		use_proxy: 1,
		collected_data: 1,
	}
};

axios(options)
	.then(response => {
		console.log(response.data);
	});`
	},


	get_go: (url) => {
		return `
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"net/url"
)

func main() {

	baseUrl, err := url.Parse("${url}")

	params := url.Values{}
	params.Add("input", "Bart Simpson")
	params.Add("filter_input", "1")
	params.Add("use_proxy", "1")
	params.Add("collected_data", "1")
	baseUrl.RawQuery = params.Encode()

	response, err := http.Get(baseUrl.String())

	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(responseData))

}`
	}
}

// ------------------ //

export var jobtitle_examples = {


	get_py: (url) => {
		return `
import requests

url = '${url}'

payload = {
	'input': 'Bart Simpson',
	'filter_input': 0,
	'use_proxy': 1,
	'ner_threshold': 0.95,
	'country_code': 'us',
}

response = requests.get(url, params=payload)
print(response.json())`
},


	get_bash: (url) => {
		return `
curl -G "${url}" \\
--data-urlencode "input=bart simpson" \\
--data-urlencode "filter_input=0" \\
--data-urlencode "use_proxy=1" \\
--data-urlencode "ner_threshold=0.95" \\
--data-urlencode "country_code=us"`
	},


	get_js: (url) => {
		return `
import axios from "axios"

const options = {
	url: '${url}',
	method: 'GET',
	data: {
		input: "bart simpson",
		filter_input: 1,
		use_proxy: 1,
		ner_threshold: 0.95,
		country_code: "us"
	}
};

axios(options)
	.then(response => {
		console.log(response.data);
	});`
	},


	get_go: (url) => {
		return `
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"net/url"
)

func main() {

	baseUrl, err := url.Parse("${url}")

	params := url.Values{}
	params.Add("input", "bart simpson")
	params.Add("filter_input", "1")
	params.Add("use_proxy", "1")
	params.Add("ner_threshold", "0.95")
	params.Add("country_code", "us")
	baseUrl.RawQuery = params.Encode()

	response, err := http.Get(baseUrl.String())

	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(responseData))

}`
	}
}
