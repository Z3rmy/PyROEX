1. Requirements
   
    1.1 Environment

        OS: Windows, Linux, Mac (64 - bit)
        Memory: Min 512MB
        Disk: Min 500MB
        Built with Conda 24.11.3, Python 3.11.7, Spyder 6.0.0

    1.2 License

        GNU General Public License (Version 3).

3. Installation
   
    Extract PyROEX.zip using 【7z x PyROEX.zip】 (Windows cmd) or 【unzip PyROEX.zip -d target_folder】 (Linux/Mac terminal).
    Navigate to src folder in terminal and run 【pip install -r requirements.txt】.
    Run 【Python main.py】 to start the software.

5. Functions

    3.1 Data Monitoring

        Import ROEX file, select type (atmospheric/ionospheric).
        Set SNR thresholds.
        Plot original data or data changing rate.

    3.2 Data Combination

        Plot data combinations (MW, GF, IF, DIF) for quality check.

   3.3 Data Integrity
      Check the completeness of the data.

    3.3 File Cutting
   
        Input time parameters and output file name.
        Click "Execute" to generate a new ROEX file.
