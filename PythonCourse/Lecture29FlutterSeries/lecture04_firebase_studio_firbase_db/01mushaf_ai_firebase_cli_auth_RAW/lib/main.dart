import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:myapp/LRS.dart';
import 'package:myapp/firebase_options.dart';
import 'package:quran/quran.dart' as quran;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(debugShowCheckedModeBanner: false, home: LoginScreen());
  }
}

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar( title: Text("Mushaf"),
      
      actions: [
        IconButton(onPressed:() async{
await FirebaseAuth.instance.signOut();

          Navigator.push(context, MaterialPageRoute(builder: (context)=>LoginScreen()));
        }, icon: Icon(Icons.logout))

      ],
      
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Center(child: Text("Mushaf")),

            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SurahContents()),
                );
              },
              child: Text("Get Started "),
            ),
          ],
        ),
      ),
    );
  }
}

class SurahContents extends StatefulWidget {
  const SurahContents({super.key});

  @override
  State<SurahContents> createState() => _SurahContentsState();
}

class _SurahContentsState extends State<SurahContents> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: 114,
        itemBuilder: (context, index) {
          return ListTile(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => DetailSurah(index + 1)),
              );
            },
            title: Text(
              quran.getSurahNameArabic(index + 1),
              textAlign: TextAlign.right,
              style: GoogleFonts.amiri(),
            ),
            subtitle: Text(
              quran.getSurahName(index + 1),
              textAlign: TextAlign.right,
              style: GoogleFonts.amiri(),
            ),
          );
        },
      ),
    );
  }
}

class DetailSurah extends StatefulWidget {
  var surahnum;
  DetailSurah(this.surahnum, {super.key});

  @override
  State<DetailSurah> createState() => _DetailSurahState();
}

class _DetailSurahState extends State<DetailSurah> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: quran.getVerseCount(widget.surahnum),
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(
              quran.getVerse(widget.surahnum, index + 1, verseEndSymbol: true),
              textAlign: TextAlign.right,
              style: GoogleFonts.amiri(),
            ),
          );
        },
      ),
    );
  }
}
