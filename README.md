<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pratyushvshah/TheGroundFoor">
    <img src="logo.ico" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">The GroundFloor™</h3>

  <p align="center">
    A CLI for texting your friends
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is aimed towards creating a fast, secure, lightweight CLI for texting your friends. No more Mr. Zuckerberg stealing your data. The project makes use of multi-threading and PostgreSQL to send and receive messages from 2 clients.

### Features

1. Login/Create user (Supporting hashing of passwords)
1. Notifications for friend requests and unread messages
1. Sending friend requests, accepting/declining friend requests
1. Removing friends
1. Starting chatrooms (Supporting AES Encryption, can only send messages to your friends)
1. Plays a sound upon receiving a message
1. Changing default settings (Number of messages displayed upon starting chat room, etc.)

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

1. Python
1. PostgreSQL

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

1. Use the `log.sql` file in the directory get the commands through which you can create your own database.
1. You can host the database on a platform like [bit.io](https://bit.io/).
1. After hosting the database, update the connection url in the `main.py` file on line 15.
1. Update your secret keys on lines 20 - 22. The "encryptkey" and "iv" keys are used to encrypt and decrypt the messages and MUST be 16 bytes long.
1. Voila! You can now text your friends using this CLI. Just send the `main.py` file to your friends or you can convert it to a `.exe` file and send it as an application!

### Prerequisites

Go to the directory where you downloaded the project and run the following command in the terminal:

```bash
pip install -r requirements.txt
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

There's no instructions, just run `main.py` in your terminal and follow the instructions on the screen!
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Remember the user so they don't have to log in again (after converting `main.py` to an .exe file)
- [ ] Allow sending images, videos, and audio files to your friends.
- [ ] Add an error log
- [ ] Make the UI more friendly and add color.
- [ ] Add a way to send messages to a group.

See the [open issues](https://github.com/pratyushvshah/TheGroundFoor/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- DISCLAIMER -->
## Disclaimer

None of the contributors of TheGroundFloor, in any way whatsoever, can be responsible for your use of the code, CLI, or the website.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Pratyush Shah - <a href = "mailto: abc@example.com">Email</a>, [LinkedIn](https://www.linkedin.com/in/pratyushvshah/)

Project Link: [https://github.com/pratyushvshah/TheGroundFoor](https://github.com/pratyushvshah/TheGroundFoor)

<p align="right">(<a href="#top">back to top</a>)</p>