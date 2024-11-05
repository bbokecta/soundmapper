### Overview

The SoundMapper code takes two user-inputted addresses and creates a Spotify playlist with songs from artists that have performed in either location. 

### Installation

1. You'll need to sign up to the following programs to get your API key:

   - [Geocode](https://geocode.maps.co/)

   - [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)

2. Once you get the keys, put each one in a separate .txt file with the following names:

   - geocode_keys.txt

   - ticketmaster_keys.txt

3. You'll also need your Spotify developer information, with the keys matching the below names:

   - username

   - client_id

   - client_secret

   - redirect

4. Download the requirements.txt file from my repo and add it to the same directory as you've put your Geocode, Ticketmaster and Spotify keys
5. Download my source code (SoundMapper.ipynb) and add this to the same directory
6. Activate a virtual environment in the directory

### Usage

When you run the SoundMapper code, you'll be prompted to input a starting address and a destination address. These can be as detailed as a full letterhead address (if you include the country, use the **ISO alpha-2 code** only! ex: US, not USA or America)

You'll then be prompted to select one genre only, in lowercase letters.

And if all goes according to plan, your brand new playlist should open in your browser!

