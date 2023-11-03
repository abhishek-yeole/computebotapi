[![ComputeGPT](https://i.ibb.co/WnSy5n2/Road-Sense-removebg-preview.png)](https://computegpt.vercel.app/)
# ComputeGPT
### Welcome to ComputeGPT - Your Computational Companion.

ComputeGPT is your one-stop solution for accurate and efficient mathematical problem-solving, powered by advanced LLM technology.

### Our Mission

At ComputeGPT, our mission is to simplify complex mathematical problem-solving for users worldwide. We strive to provide a seamless and intuitive experience, enabling users to solve intricate computations effortlessly.

### Features

- Step by step solution to Math-related problems:
  > ComputeGPT offers a step-by-step breakdown of even the most intricate mathematical problems, ensuring a comprehensive understanding of the solution process.

- LLM powered solutions:
  > Empowered by the latest in Language Model technology, ComputeGPT provides highly accurate and reliable solutions to a diverse range of computational challenges.

- Speech/Voice interface:
  > Interact with ComputeGPT effortlessly using our intuitive voice interface. Ask complex math queries verbally and receive immediate, accurate responses.

- Conversation Bot:
  > Engage in a seamless conversation with ComputeGPT. Enjoy a continuous interaction experience as ComputeGPT comprehends and responds to your queries in a natural, conversational manner.

## Visit Live Site

ComputeGPT is hosted using Vercel.

_[ComputeGPT](https://computegpt.vercel.app/)_

## Run it locally using your own Wolfram | Alpha Keys

In the project directory, you can run:
### `python -m venv c:\path\to\project`
Setups the virtual Environment to start the runtime.

### `pip install -r requirements.txt`

Installs the required the libraries on the local machine. Also install required libraries if not installed use:

> **NOTE:** Python version must be higher than 3.9. The project was developed on 3.11 python version.

### Use your own keys to run the API's

- Update the `index.py` file in the api folder.
- Change the `os.environ.get('WOLFRAM_STEPS_KEY')`, others..., with your own keys for that particular `app_id`.

### `flask --app main run --host 0.0.0.0`

Runs the app in the development mode. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) to view it in your browser.

> **NOTE:** These are the API's endpoints that are developed. If you want to test the API's you can either change the config.jsx api Url's with `http://your-ip-address:5000/...` in the frontend of [https://github.com/abhishek-yeole/computegpt/blob/main/src/config.jsx](https://github.com/abhishek-yeole/computegpt/blob/main/src/config.jsx) or use POSTMAN or other services for it.
