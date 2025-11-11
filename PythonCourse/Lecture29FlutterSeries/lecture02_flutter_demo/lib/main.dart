import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    TextEditingController userName = TextEditingController();
    TextEditingController userEmail = TextEditingController();
    TextEditingController userPass = TextEditingController();
    return MaterialApp(
      home: Scaffold(
        // backgroundColor: Colors.blue,
        body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              TextField(
                controller: userName,
                keyboardType: TextInputType.text,
                decoration: InputDecoration(
                  hint: Text("Enter Your Name Here"),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10)),
                  ),
                ),
              ),
              SizedBox(height: 10),
              TextField(
                controller: userEmail,

                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  hint: Text("Enter Your Email Here"),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10)),
                  ),
                ),
              ),
              SizedBox(height: 10),
              TextField(
                controller: userPass,
                obscureText: true,
                obscuringCharacter: "#",
                keyboardType: TextInputType.phone,
                decoration: InputDecoration(
                  hint: Text("Enter Your Password Here"),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.all(Radius.circular(10)),
                  ),
                ),
              ),

              SizedBox(height: 20),

              ElevatedButton(
                onPressed: () {
                  String name = userName.text.toString();
                  String email = userEmail.text.toString();
                  String pass = userPass.text.toString();

                  print("Student Name $name");
                  print("Student Email $email");
                  print("Student Password $pass");
                },
                child: Text("Submit"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
