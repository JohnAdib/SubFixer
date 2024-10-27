# **SubFixer**

SubFixer is a Python package designed to manage and synchronize subtitle files. Whether you need to shift subtitle timings, adjust frame rates, or translate subtitles into different languages, SubFixer provides an easy and efficient way to do it all.

## **Features**
- **Shift Subtitle Timings**: Synchronize subtitles by shifting them forward or backward by a specified number of seconds.
- **Change Frame Rate**: Adjust the subtitle timings based on different frame rates for compatibility.
- **Subtitle Translation** (Upcoming): Translate subtitles into various languages.
- **Support for SRT Format**: Works seamlessly with `.srt` files, the most commonly used subtitle format.

## **Installation**

To install SubFixer, clone this repository or download the source code:

```bash
git clone https://github.com/yourusername/SubFixer.git
```

Then, navigate to the directory and install the requirements:

```bash
cd SubFixer
pip install -r requirements.txt
python3 subfixer.py input.srt output.srt 00:03:40
```

## **Usage**

### **Shift Subtitle Timings**
Shift subtitles by a specified number of seconds (positive for delay, negative for advance).

## **Contributing**

Contributions are welcome! If you have ideas for improving the package or would like to add new features, please feel free to submit an issue or a pull request.

## **Roadmap**
- [x] Shift subtitle timings
- [ ] Adjust frame rates for subtitle synchronization
- [ ] Add translation support for multiple languages

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
