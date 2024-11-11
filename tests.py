from click.testing import CliRunner
import main

def tests():
    runner = CliRunner()
    try:
        #######################Checks for successful test#######################
        monthTest = runner.invoke(main.monthly, "2021-02")
        assert monthTest.exit_code == 0
        dayTest = runner.invoke(main.daily, "2021-02-14")
        assert dayTest.exit_code == 0
        
        ###########Checks for failed test without critical error################
        monthTestFailed = runner.invoke(main.monthly, "2022-02")
        assert monthTestFailed.exit_code == 0
        dayTestFailed = runner.invoke(main.daily, "2021-13-14")
        assert dayTestFailed.exit_code == 0

        ###########Checks for invalid usage of the commands#####################
        dateMonthTest = runner.invoke(main.monthly, "2022")
        assert dateMonthTest.exit_code == 2
        dateDayTest = runner.invoke(main.daily, "2054s-sjsj")
        assert dateDayTest.exit_code == 2
        print("Successful testing")
    except:
        print("Failed")

if __name__ == '__main__':
    tests()