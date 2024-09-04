#include <stdio.h> 
#include <strings.h> //bzero
#include <sys/types.h> 
#include <arpa/inet.h> //htonl, htons
#include <sys/socket.h> 
#include<netinet/in.h> //struct sockaddr_in

#define PORT 8080

/*
    These are the struct definitions used in the code:

    struct sockaddr_in {
        sa_family_t    sin_family; // Address family (AF_INET for IPv4)
        in_port_t      sin_port;   // Port number (network byte order)
        struct in_addr sin_addr;   // IPv4 address
    };

    struct in_addr {
        uint32_t       s_addr;     // IPv4 address (network byte order)
    };
    */

int main() 
{ 
    char buffer[100]; //Buffer to store recvd message.
    int sockfd; //File descriptor for the socket. 
    struct sockaddr_in server_addr, client_addr; //Declare server address struct.
    int client_addr_len = sizeof(client_addr); //Length of the client address struct
    ssize_t number_of_bytes_received; //Number of bytes received from the client.
    bzero(&server_addr, sizeof(server_addr)); //Clears the server address structure to avoid any garbage values.

	// Create a UDP Socket 
    sockfd = socket(AF_INET, SOCK_DGRAM, 0); //Create a socket with the following parameters: 
                                                //AF_INET: IPv4 Internet protocols
                                                //SOCK_DGRAM: UDP SOCKET TYPE
                                                //0: Protocol value for Internet Protocol (IP).	 
	
    
    server_addr.sin_family = AF_INET; //Set the address family to IPv4.
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
    /*INADDR_ANY is a constant that represents the IPv4 address 0.0.0.0. 
    The htonl function converts this address to network byte order, 
    which is necessary for network communication.*/

    //uint16_t htons(uint16_t hostshort);
    /*The htons() function converts the unsigned short integer hostshort from host byte order 
      to network byte order.*/
	server_addr.sin_port = htons(PORT); 
  
    /* Binding in the context of network programming refers to associating a socket 
       with a specific local IP address and port number.
        The bind system call is used to bind the server's address  
        to the socket descriptor (sockfd). 
        The kernel creates an internal data structure that maps the specified IP address and port number 
        to the socket file descriptor.*/
	bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)); 
    
    //Vulnerable (Bad implmentation). Third argument should be sizeof(buffer).
    number_of_bytes_received = recvfrom(sockfd, buffer, 1000, 0, (struct sockaddr*)&client_addr,&client_addr_len); //receive message from server
    
	buffer[number_of_bytes_received] = '\0'; //Adds a null terminator to the received message to ensure 
    //it is treated as a proper C string. (Assumes the exact size of the message was writen to the buffer)
	
    printf("Client : %s\n", buffer); //Prints the received message to the console.

	const char *response = "Software Engineering and Cybersecurity Laboratory\nMontana State University\nSchool of Computing\nPO Box 173880\nBozeman, MT 59717\n"; //Message to send to client.
    sendto(sockfd, response, 1000, 0, (struct sockaddr*)&client_addr, sizeof(client_addr)); 
    close(sockfd); //Close the socket.
    
    return 0;
} 
