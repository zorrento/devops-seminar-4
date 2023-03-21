from flask import Flask, request
import requests
import ast
response = requests.get("https://google.com")
print("Type:")
print(response.text)