import sys, os, requests
import tkinter as tk
from tkinter import messagebox

# Console GUI
class Display(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)		
        self.parent = parent

        self.output = tk.Text(self, width=100, height=15, background = 'black', fg='white')
        self.output.pack(side=tk.LEFT, fill='both', expand=1)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command = self.output.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.output['yscrollcommand'] = self.scrollbar.set

        self.count = 1
        self.configure(background='black')
        self.pack(fill='both', expand=1)
        #self.wait_window()
        #self.thecode = thecode(self)
        #self.thecode.func_install(self)
		
    def printcmd(self, txt):
        self.output.insert(tk.END,str(txt))
        self.output.insert(tk.END,'\n')
        self.output.see(tk.END)
        self.update_idletasks()

    def askuserbox(self, message):
        askbox = messagebox.askyesno('Question', message)
        return askbox
    	
    def call_close(self, parent):
        messagebox.showinfo('quit', "Quitting.")
        parent.killing_root()
    
    # Python version
    def pythoncheck(self):
        # Require Python 3 to work
        if sys.version_info.major < 3:
            raise PythonVersionError
            return 1
        else:
            self.printcmd("OK:	Python version.")
            return 0

    # Import pip installer
    def pipimport(self):
        try:
            pip = __import__('pip')
            self.printcmd("OK:	Pip")
        except ModuleNotFoundError:
            return 1
        try:
            from pip._internal import main as pipmain
        except:
            from pip import main as pipmain
        self.pipmain = pipmain
        return 0

    # SimCav
    def list_simcav_modules(self):
        simcav_files = ['simcav_main.py', 'simcav_CavityComputation.py', 'scrolledframe.py', 'simcav_ElementFeatures.py', 'simcav_abcd.py', 'simcav_simulator.py', 'tooltips.py', 'simcav_uninstaller.py', 'simcav_updater.py', 'misc.py']
        return simcav_files

    def list_simcav_misc(self):
        simcav_misc = ['LICENSE', 'Disclaimer.txt', 'README.md', 'CHANGELOG']
        return simcav_misc
        
    def list_simcav_icons(self):
        simcav_icons = []
        simcav_api = self.get_api()
        # Get icons list from repo
        r = requests.get(simcav_api+'tree?ref=master&per_page=100', params={'path':'Icons/'})
        for i in r.json():
            if not '.svg' in i['name']:
                simcav_icons.append(i['name'])
        return simcav_icons
        
    def list_simcav_saves(self):
        simcav_saves = []
        simcav_api = self.get_api()
        # Get icons list from repo
        r = requests.get(simcav_api+'tree?ref=master&per_page=100', params={'path':'Saves/'})
        for i in r.json():
            simcav_saves.append(i['name'])
        return simcav_saves
                
    def gethomepath(self, theguestOS):
        # Get paths
        if theguestOS == 'win32':
            user_home = self.winshell.folder("profile")
        else:
            user_home = os.path.expanduser('~')
        simcav_home = os.path.join(user_home, 'SimCav')
        return simcav_home

    # URL functions
    def get_api(self):
        api_url = 'https://gitlab.com/api/v4/projects/6789132/repository/'
        return api_url

    def get_repo(self):
        repo_url = 'https://gitlab.com/simcav/simcav/raw/master/'
        return repo_url
        
    # DOWNLOADS
    # Download a file
    def download_manual(self, simcav_home):
        import urllib.request
        simcav_url = self.get_repo()
        url = simcav_url + 'Manual/manual.pdf'
        folderfile = os.path.join(simcav_home, 'manual.pdf')
        try:
            urllib.request.urlretrieve(url, folderfile)
            return 0
        except:
            raise
            return 1

    def download_file(self, thefile, thefolder):
        import urllib.request
        simcav_url = self.get_repo()
        if os.path.basename(thefolder) in ['Icons', 'Saves']:
            url = simcav_url + os.path.basename(thefolder) + '/' + thefile
        else:
            url = simcav_url + thefile
        folderfile = os.path.join(thefolder, thefile)
        try:
            self.printcmd("     Downloading " + thefile)
            urllib.request.urlretrieve(url, folderfile)
            return 0
        except:
            raise WebFileError(thefile)
            return 1

    def download_group(self, onegroup, group_folder):
        for i in onegroup:
            download_error = self.download_file(i, group_folder)
            if download_error:
                self.printcmd('Error downloading ' + i)
                raise
                return 1
        return 0
        
    # Download all files
    def download_simcav(self, simcav_home):
        #Downloading SimCav files
        self.printcmd('\n Downloading modules...')
        simcav_modules = self.list_simcav_modules()
        self.download_group(simcav_modules, simcav_home)

        self.printcmd('\n Downloading icons...')
        simcav_icons = self.list_simcav_icons()
        self.download_group(simcav_icons, os.path.join(simcav_home,'Icons'))
            
        self.printcmd('\n Downloading examples...')
        simcav_saves = self.list_simcav_saves()
        self.download_group(simcav_saves, os.path.join(simcav_home,'Saves'))
        
        self.printcmd('\n Downloading other files...')
        simcav_misc = self.list_simcav_misc()
        self.download_group(simcav_misc, simcav_home)
            
        self.printcmd('\n Downloading manual...')
        download_error = self.download_manual(simcav_home)
        self.printcmd('\n Files downloaded')

    # Installing functions
    def guestOS(self):
        return sys.platform
        
    def pipinstall(self, package):
    	self.printcmd("\n ---------------------\n Installing " + package)
    	try:
    		pipcode = self.pipmain(['install', package, '--user', '--disable-pip-version-check', '--no-warn-conflicts'])
    		if not pipcode:
    			return True
    		else:
    			return False
    	except Exception as inst:
    		self.printcmd(inst)
    		self.printcmd("Error")
    		return False
            
    def pipuninstall(self, package):
    	try:
    		self.pipmain(['uninstall', package, '-y', '--disable-pip-version-check'])
    		return True
    	except Exception as inst:
    		self.printcmd(inst)
    		self.printcmd("Error")
    		return False
    
    def install_winshell(self):
        try:
            import winshell
        except:
            self.pipimport()
            haveIinstalled = self.pipinstall('winshell')
            if haveIinstalled:
                import winshell
            else:
                self.printcmd("Error: Couldn't install Winshell")
                raise
                return 1
        else:
            self.winshell = winshell
            self.printcmd("OK: Winshell")
            return 0

# Defining exceptions
class PythonVersionError(Exception):
	def __init__(self):
		self.expression = "\nError: Incompatible Python version."
		self.message = "  SimCav only works with Python 3, but an older version was detected.\n  Please update to Python 3.\n"
class PipInstallError(Exception):
	def __init__(self, package):
		self.message = "Install the package '" + package + "' manually and try again."
class NotModuleError(Exception):
	def __init__(self, package):
		self.message = "Please install '" + package + "' before installing SimCav."
class WebFileError(Exception):
	def __init__(self, thefile):
		self.message = "Error: '" + thefile + "' not found'"
class UserCancel(Exception):
	def __init__(self):
		self.expression = "\nError: Cancelled by user."
		self.message = ""