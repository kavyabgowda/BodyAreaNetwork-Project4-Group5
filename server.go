package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {

	listener, err := net.Listen("tcp", "0.0.0.0:80")
	if err != nil {
		fmt.Printf("%v", err)
		os.Exit(1)
	}

	fmt.Printf("started server\n")
	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("%v\n", err)
		}

		go handleEdge(conn)
	}
}

func handleEdge(conn net.Conn) {
	fmt.Printf("new connection: %v\n", conn.RemoteAddr())

	inBuff := bufio.NewReader(conn)
	//outBuff := bufio.NewWriter(conn)

	edgeName := ""
	for {
		message, err := inBuff.ReadString(byte('\n'))
		if err != nil {
			fmt.Printf("connection terminated: %v\n", err)
			break
		}
		n := len(message)
		for n > 0 && (message[n-1] == '\n' || message[n-1] == '\r') {
			n--
		}
		message = message[:n]

		if strings.HasPrefix(message, "NEWEDGE ") {
			edgeName = message[8:]
			fmt.Printf("connection with: %s\n", edgeName)

		} else if strings.HasPrefix(message, "UPDATE ") {
			info := strings.SplitN(message[7:], " ", 2)
			if len(info) < 2 {
				if edgeName != "" {
					fmt.Printf("%s - unknown message: %s\n", edgeName, message)
					continue
				}
			}
			deviceName := info[0]
			deviceMessage := info[1]

			fmt.Printf("%s:%s: %s\n", edgeName, deviceName, deviceMessage)

		} else {
			if edgeName != "" {
				fmt.Printf("%s - unknown message: %s\n", edgeName, message)
			} else {
				fmt.Printf("unknown message: %s\n", message)
			}
			continue
		}
	}
	conn.Close()
}
