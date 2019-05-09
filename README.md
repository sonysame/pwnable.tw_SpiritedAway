# pwnable.tw_SpiritedAway  
## House Of Spirit!  

문제는 다음과 같다.  
1. enter your name: buf(60바이트까지)  
2. etner your age: v5 scanf  
3. Why did you came to see this movie?: v7(80바이트까지): leak 가능(스택영역, 힙영역)  
4. comment: s(60바이트까지)  

print(name, age, reason, comment)  
choice: Y/y -> free(buf)  

0xbfffed10:~~~~  
0xbfffed48: nbytes(0x3C)  
0xbfffed4c: v3(0x50)  
0xbfffed50: s   : comment(0x3c)  
0xbfffeda0: v5  : age  
0xbfffeda4: buf : 0x804b410:name   
0xbfffeda8: v7  : why(0x50)-> leak 가능(스택영역, 힙영역)~/0xbfffedf8  
0xbfffedfc: ret  

nbytes를 덮을 수 있다.  
3C->6E  

comment를 0x6E만큼 즉, buf를 덮을 수 있다. 결국 우리가 원하는 곳을 free시킬 수 있다!  


<시나리오>  
1. why부분으로 스택영역 주소, 힙영역 주소 leak  
2. cnt 100으로 만들어서 buf에 원하는 주소 넣는다.(n이 0x3c->0x6e로 바뀌면서 buf까지 도달가능)    
3. why 부분에 fake chunk를 만들어준다!  

첨부된 HouseOfSpirit은 32비트 환경에서 House Of Spirit 시나리오를 보여준다.  
fake chunk size: 0x44  
0xbfffedac:	0x00000040  
0xbfffedec:	0x00000123  

4. free를 시켜준다.(malloc(0x3C)에 맞게끔)  
5. name을 넣어줄 때, ret을 덮는다! 
