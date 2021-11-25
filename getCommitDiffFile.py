#!/usr/bin/env python3

import subprocess
from subprocess import PIPE
import git

targetDir = ""

#mainブランチのコミットID（Short）を取得
TopCommitID = subprocess.run("git rev-parse --short HEAD",cwd=targetDir, shell=True, stdout=PIPE, stderr=PIPE, text=True).stdout
TopCommitID = TopCommitID.replace( '\n' , '' )

#mainブランチのコミット総数の取得
mainCommitCount = subprocess.run("git rev-list --count main",cwd=targetDir, shell=True, stdout=PIPE, stderr=PIPE, text=True).stdout
mainCommitCount = int(mainCommitCount)

nowCommitHead = TopCommitID
pastCommitHead = ""
count = 1

while count < mainCommitCount:
	
	if count != 1:
		subprocess.run("git switch -d HEAD~",cwd=targetDir,shell=True)
		#前回のコミットの変更前のファイルの取得
		commandB  = 'git checkout-index -f --prefix=archive/'+str(pastCommitHead)+'_b/ '+'`git diff --name-only '+pastCommitHead +' '+ pastCommitHead+'~`'
		subprocess.run(commandB,cwd=targetDir,shell=True)
	
	if count != mainCommitCount:
		nowCommitHead = subprocess.run("git rev-parse --short HEAD",cwd=targetDir, shell=True, stdout=PIPE, stderr=PIPE, text=True).stdout
		nowCommitHead = nowCommitHead.replace( '\n' , '' )
		#switch後の現在のコミットとその一個前のもの参照
		commandA  = 'git checkout-index -f --prefix=archive/'+str(nowCommitHead)+'_a/ '+'`git diff --name-only '+nowCommitHead +' '+ nowCommitHead+'~`'
		subprocess.run(commandA,cwd=targetDir,shell=True)
		pastCommitHead = nowCommitHead

	count += 1

print("処理が終わったので元のHEADに戻します。")
subprocess.run("git switch -d "+str(TopCommitID),cwd=targetDir,shell=True)
