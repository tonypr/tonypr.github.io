---
title: "Quick Self-Hosted LLM Set Up"
date: 2024-09-07T13:09:47-04:00
draft: true
summary: "Set up an LLM with secure remote access."
---

## Intro 


This past Labor day I found myself with some extra time and some Large Language Model (LLM) DIY inspired motivation from watching this thorough [3-hour LLM workshop](https://www.youtube.com/watch?v=quh7z1q7-uc). That motivated me to try out running an LLM and setting up a self-hosted LLM environment. I found the workshop to be great! If you're interested in taking a closer look at how LLMs work, give it a watch!

I'm pretty impressed with all the tools used and figured I'd share in case others might interested.

If all steps work out you should be able to access your self-hosted LLM from any device connected to your VPN. For example, on my phone it looks like this:


<div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
  <video width="40%" controls autoplay>
    <source src="./media/screenrecord.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>


### Step-by-Step Set Up Guide

Here's the breakdown of the relevant steps for self-hosting an LLM and making it accessible remotely without having to expose your server to the open web.

> Note: Before you get started, ensure your system has enough resources to run an LLM. The requirements change depending on the size of the model you want to run and additional configurations.

This guide assumes you already have Python installed and are comfortable with running commands on the command line. I went through these steps on Ubuntu, you might need to adjust the steps for other operating systems.

**Overview**

1. **Set Up Your Local LLM**
    1. Install `litgpt`.
    1. Start serving model (e.g. `microsoft/phi-2`).
1. **Set Up Your LLM UI**
    1. Install `flask`.
    1. Run UI webserver.
1. **Set Up Secure Remote Access**
    1. Set up a VPN.
    1. Connect your devices.
1. **Check Out Your Setup**
    1. Connect to your LLM UI through a remote device.
    1. Test it out!



## Set Up Your Local LLM 🤖
### Install

First, install the `litgpt` tool so that you can easily download and run open LLM models. Full instructions available at the [litgpt repo](https://github.com/Lightning-AI/litgpt).

```bash
$ pip install 'litgpt[all]'
```

You can run a server that handles prompt request by using the `serve` command. It'll also go through the process of downloading the model you specify if you haven't downloaded it yet.
```bash
$ litgpt serve microsoft/phi-2
```
### Test

You can also try out test prompts with the model using either the `generate` or `chat` commands:
```bash
$ litgpt generate microsoft/phi-2 --prompt "How many days are there in December, 2024?"
```


Use an interactive chat
```bash
$ litgpt chat microsoft/phi-2
```

### Other Models & Configurations
I found the `microsoft/phi-2` model to be easy to set up but pretty inaccurate. I ended up using `meta-llama/Meta-Llama-3.1-8B-Instruct` instead. If you choose to use Llama models, know that before you can download them you need to request access to the models on the [huggingface](https://huggingface.co/) website. 

If you try running the Llama model and encounter GPU out-of-memory issues you can apply [quantization](https://github.com/Lightning-AI/litgpt/blob/1d37f9a99bb4ba2b7373bc7fc5b8c5a457af48df/tutorials/quantize.md#bnbnf4-dq) to reduce the memory footprint. With the Llama model the command might look like this:

```
$ litgpt serve meta-llama/Meta-Llama-3.1-8B-Instruct \
    --quantize bnb.nf4-dq \
    --precision bf16-true \
    --max_new_tokens 256
```


## Set Up Your LLM UI 🖥️
For this setup, I used a simple Flask server to run the UI, which communicates with the LLM backend through HTTP requests.

### Install Dependencies
First, you'll need to install Flask, a lightweight web framework for Python that makes setting up a web server straightforward. Then install the `requests` library which our Flask app will use to communicate with the litgpt server.

```
$ pip install Flask
$ pip install requests
```

### Server Code

For the server code, my simple app code has this structure:
```bash
$ tree
.
├── app.py
└── templates
    └── index.html
```

You can find the sources here:
- [app.py](./source/app.py)
- [index.html](./source/templates/index.txt)

Note, if using this code, follow the directory structure as Flask expects the template file to be under the templates directory.

Once you have the code in place, start your server:
```bash
$ python app.py
```

You should be able to navigate to your [localhost:5000](http://localhost:5000/) page and see the UI.

## Enable Secure Remote Access

If you don't intend on accessing your self-hosted LLM remotely, skip this step.

Install [tailscale](https://tailscale.com/).
