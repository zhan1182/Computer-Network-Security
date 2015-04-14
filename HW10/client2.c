/*
/ file : client2.c
/--------------------------------------------------------------------------
/
/ This is the client side of the server-client pair for the buffer overflow 
/ homework in Lecture 21 of ECE 404 at Purdue.
/
/ This is a client socket program that interacts with a human user and sends
/ the user-entered messages to the server.  This program is meant to be used 
/ with server2.c serving as the server. Initially run the server in one window 
/ and the client in another window on the same machine by issuing calls like
/
/      server2 9000
/
/      client2 localhost 9000
/
/ Subsequently, run the server on one of the ECN machines and the client 
/ on your laptop.
*/


// For compiling this file:
//
//        Linux:               gcc client2.c -o client2
//
//        Solaris:             gcc client2.c -o client2 -lsocket -lnsl
//
// Solaris needs to be explicitly told about the libraries libsocket and 
// libnsl.  The latter library is for "Network Service Library"; it has
// the implementation code for functions such as gethostbyname(), etc.
//
// For running this client socket program:
//
//                client2  RVL4.ecn.purdue.edu  9000
//
// assuming that the server is running on the host RVL4.ecn.purdue.edu and
// that the server is monitoring port 9000. 
//
// Code originally pulled off the internet a long time back and then modified by 
// Avi Kak on April 12, 2014.  The modifications made are very minor --- basically
// dealing with interrupt handling, etc.


#include <signal.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <errno.h> 
#include <string.h> 
#include <strings.h>         // for bzero(), bcopy()
#include <sys/socket.h> 
#include <arpa/inet.h>
#include <netdb.h>           // for gethostbyname() etc.
//#include <netinet/in.h> 
//#include <sys/types.h> 

#define MAX_DATA_SIZE 4096
 
int main(int argc, char *argv[]) {
    int sockfd;
    int recvSize;  
    char buff[MAX_DATA_SIZE];
    char sendData[MAX_DATA_SIZE];
    struct sockaddr_in servAddr; 
    struct hostent *server;
    void SIGINThandler(int);

    signal(SIGINT, SIGINThandler);

    if (argc != 3) {
	fprintf(stderr,"Usage:    %s   server_hostname_or_ip_addr   port\n", argv[0]);
	exit(1);
    }
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
	perror("socket");
	exit(1);
    }
    int PORT = atoi(argv[2]);
    server = gethostbyname(argv[1]);
    if (server == NULL) {
        fprintf(stderr, "The server host does not exist\n");
        exit(0);
    }
    // Avi comment: First initialize the server socket number
    bzero((char*) &servAddr, sizeof(servAddr));
    servAddr.sin_family = AF_INET;      
    servAddr.sin_port = htons(PORT);    
    bcopy((char*) server->h_addr,
          (char*) &servAddr.sin_addr.s_addr, server->h_length);
    if (connect(sockfd, (struct sockaddr *)&servAddr, sizeof(servAddr)) == -1) {
	perror("connect failed");
	exit(1);
    }
    if ((recvSize = recv(sockfd, buff, 30, 0)) == -1) {
	perror("recv failed");
	exit(1);
    }

    buff[recvSize] = '\0';
    printf("%s", buff);

    /* repeat until "exit" input */
    while(1) {
        printf("Say something: ");
        fgets(sendData, MAX_DATA_SIZE, stdin);
        /* if input is "exit", terminate this program */
        if(!strncmp(sendData, "exit", 4)) {
            close(sockfd);
            exit(0);
        }
        if (send(sockfd, sendData, strlen(sendData), 0) == -1) {
            perror("send failed");
            close(sockfd);
            exit(1);
        }
        if ((recvSize = recv(sockfd, buff, MAX_DATA_SIZE, 0)) == -1) {
            perror("recv failed");
            exit(1);
        }
        buff[recvSize] = '\0';
        printf("You Said: %s\n", buff);
    }
    close(sockfd);

    return 0;
}

void SIGINThandler(int sig) {
    printf("Terminating the client process id %d\n", getpid());
    exit(0);
}
    
