import pickle

secret_tips = [r'''Keep your software up to date: 
               Regularly update your operating system, 
               antivirus software, web browsers, and 
               other applications to ensure you have 
               the latest security patches. This helps 
               protect against known vulnerabilities that 
               malware can exploit.'''

,r'''Use a reputable antivirus/anti-malware
 program: Install a reliable antivirus or
anti-malware software on your device and 
keep it updated. Run regular scans to 
detect and remove any malicious software.'''

,r'''Be cautious with email attachments 
and downloads: Exercise caution when opening 
email attachments or downloading files 
from the internet. Only download files from 
trusted sources, and be wary of suspicious 
or unexpected email attachments, especially 
from unknown senders.'''

,r'''Enable automatic software updates: 
Configure your operating system and 
applications to automatically download and 
install updates. This ensures that you have 
the latest security patches without having 
to manually check for updates.'''

,r'''Be careful with links: Avoid clicking 
on suspicious links, especially in emails, 
social media messages, or pop-up windows. 
Hover your mouse over a link to see the 
actual URL before clicking on it. If it 
looks suspicious or unfamiliar, avoid clicking 
on it.'''

,r'''Use strong and unique passwords: 
Create strong passwords that are difficult 
to guess and use a unique password for each 
of your online accounts. Consider using a 
password manager to securely store and generate 
passwords.'''

,r'''Regularly back up your data: 
Perform regular backups of your important 
files and data. In the event of a malware 
infection, having backups can help you restore 
your system to a clean state without losing 
your valuable information.'''

,r'''Exercise caution with public Wi-Fi: 
Public Wi-Fi networks can be insecure, making 
it easier for attackers to intercept your data. 
Avoid accessing sensitive information or logging 
into accounts that contain personal information 
when connected to public Wi-Fi.'''

,r'''Enable a firewall: 
Use a firewall to monitor and control incoming 
and outgoing network traffic. This provides 
an additional layer of security by 
blocking unauthorized connections.'''

,r'''Educate yourself: Stay informed about 
the latest types of malware, phishing techniques, 
and online scams. Be wary of social engineering 
tactics, such as emails or messages that try to 
trick you into revealing sensitive information.''',





r'''Use a strong and secure network: 
Ensure that your home Wi-Fi network 
is password protected and uses encryption 
(WPA2 or WPA3). Avoid using public Wi-Fi 
networks whenever possible, as they can be 
less secure and more vulnerable to attacks.''',

r'''Be cautious of social engineering attacks: 
Be skeptical of unsolicited phone calls, 
emails, or messages asking for personal 
information or urging you to take immediate 
action. Avoid clicking on links or 
downloading attachments from unknown 
sources.''',

r'''Enable two-factor authentication (2FA): 
Enable two-factor authentication whenever 
possible for your online accounts. This adds 
an extra layer of security by requiring a 
second form of verification, such as a unique 
code sent to your phone, in addition to your 
password.''',

r'''Be mindful of what you share online: 
Be cautious about sharing personal 
information, such as your full name, 
address, phone number, or financial 
details, on public forums, social media, 
or other websites. Limit the amount of 
personal information you make publicly 
available.''',

r'''Regularly review app permissions: 
When installing new applications on your 
devices, review the permissions they request. 
Be cautious about granting unnecessary 
permissions that could compromise your 
privacy or security.''',

r'''Be mindful of phishing emails and websites: 
Be wary of emails or websites that mimic 
legitimate organizations or services. Check 
for spelling errors, suspicious email addresses, 
or unusual website URLs. Avoid clicking on links 
in suspicious emails and manually type in the 
website address instead.''',

r'''Keep a clean and organized system: 
Regularly clean up your digital devices 
by uninstalling unnecessary applications 
and deleting files you no longer need. 
This reduces the attack surface for potential 
malware infections.''',

r'''Avoid pirated software and media: 
Downloading pirated software, movies, 
music, or other digital content from 
unofficial sources increases the risk 
of malware infection. Stick to legitimate 
and authorized sources for your software 
and media needs.''',

r'''Secure your mobile devices: 
Use a passcode, fingerprint, or facial 
recognition to lock your mobile devices. 
Install security updates and only download 
apps from reputable sources such as official 
app stores.''',

r'''Stay informed and educate others: 
Keep yourself updated about the latest 
malware threats and security practices. 
Share your knowledge with friends and family 
to help them stay protected as well.''',

r"""Be cautious of suspicious emails: 
Be skeptical of unsolicited emails, especially 
those asking for personal information or urging 
you to take immediate action. Look out for 
red flags such as generic greetings, spelling 
errors, grammatical mistakes, or email 
addresses that don't match the organization 
they claim to be from.""",

r'''Verify the source: 
If you receive an email requesting sensitive 
information or urging you to click on a 
link, independently verify the legitimacy 
of the request. Contact the organization 
directly using their official contact 
information (not the information provided 
in the email) to confirm the request.''',

r"""Don't click on suspicious links: 
Hover your mouse over links in emails 
or messages to reveal the actual URL. 
Be cautious of shortened URLs or URLs 
that appear slightly different from 
legitimate websites. If in doubt, manually 
type in the website address in your browser 
instead of clicking the link.""",

r'''Be cautious of pop-ups and ads: 
Avoid clicking on pop-up windows or ads 
that appear suspicious or unexpected, as 
they may redirect you to phishing websites. 
Consider using a pop-up blocker in your 
web browser to reduce the risk.''',

r'''Keep your browser and security 
software up to date: Regularly update your 
web browser and security software to benefit 
from the latest security patches and features 
designed to detect and block phishing attempts.''',

r'''Use strong, unique passwords: 
Create strong passwords for your online 
accounts and avoid reusing passwords 
across different platforms. This helps 
prevent attackers from gaining unauthorized 
access even if they manage to obtain 
your login credentials through a phishing 
attack.''',

r'''Enable two-factor authentication (2FA): 
Enable two-factor authentication whenever 
possible for your online accounts. This adds 
an extra layer of security by requiring a 
second form of verification, such as a 
unique code sent to your phone, in 
addition to your password.''',

r'''Educate yourself and others: 
Stay informed about the latest phishing 
techniques and share that knowledge with 
friends, family, and colleagues. Be 
especially mindful of vulnerable 
populations, such as elderly individuals 
or those who may be less familiar 
with technology.''',

r'''Use anti-phishing features: 
Some web browsers and email clients 
offer built-in anti-phishing features 
that can help identify and warn you 
about potentially malicious websites 
or emails. Enable these features and 
keep them up to date.''',

r'''Report phishing attempts: 
If you receive a phishing email or 
encounter a phishing website, report 
it to the appropriate organization or 
authorities. This helps in taking down 
the malicious content and preventing 
others from falling victim to the 
same attack'''
]

with open('Vigi_EXE/models/secret_tips.pkl', 'wb') as f:
    pickle.dump(secret_tips, f)