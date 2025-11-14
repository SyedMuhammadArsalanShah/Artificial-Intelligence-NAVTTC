

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:myapp/main.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
    TextEditingController emailLogin = TextEditingController();
         TextEditingController passwordLogin = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(body: Column(children: [

             TextField(controller: emailLogin,),
             TextField(controller: passwordLogin,),



             
             ElevatedButton(onPressed: ()async{
try {
  final credential = await FirebaseAuth.instance.signInWithEmailAndPassword(
    email: emailLogin.text,
    password: passwordLogin.text,
  ).then((value) => Navigator.push(context, MaterialPageRoute(builder: (context)=>Home())));
} on FirebaseAuthException catch (e) {
  if (e.code == 'user-not-found') {
    print('No user found for that email.');
  } else if (e.code == 'wrong-password') {
    print('Wrong password provided for that user.');
  }
}

             }, child: Text("Login")),
             ElevatedButton(onPressed: (){
              Navigator.push(context, MaterialPageRoute(builder: (context)=>SignUpScreen()));
             }, child: Text("SignUP"))

    ]));
  }
}

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
         TextEditingController emailController = TextEditingController();
         TextEditingController passwordController = TextEditingController();



  @override
  Widget build(BuildContext context) {

    return Scaffold(body: Column(children: [

             TextField(controller: emailController,),
             TextField(controller: passwordController ,),



             
             ElevatedButton(onPressed: ()async{
try {
  final credential = await FirebaseAuth.instance.createUserWithEmailAndPassword(
    email: emailController.text,
    password: passwordController.text,
  ).then((value) => Navigator.push(context, MaterialPageRoute(builder: (context)=>LoginScreen())));
} on FirebaseAuthException catch (e) {
  if (e.code == 'weak-password') {
    print('The password provided is too weak.');
  } else if (e.code == 'email-already-in-use') {
    print('The account already exists for that email.');
  }
} catch (e) {
  print(e);
}


             }, child: Text("SignUp")),
             ElevatedButton(onPressed: (){
              Navigator.push(context, MaterialPageRoute(builder: (context)=>LoginScreen()));
             }, child: Text("I have already an account "))

    ]));
    
  }
}