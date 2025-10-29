import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:quran/quran.dart' as quran;

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(title: Text("Mushaf")),

        body: ListView.builder(
          itemCount: quran.totalSurahCount,
          itemBuilder: (context, index) {
            return ListTile(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => DetailSurah(index + 1),
                  ),
                );
              },
              leading: CircleAvatar(child: Text("${index + 1}")),
              title: Text(quran.getSurahNameArabic(index + 1), style: GoogleFonts.amiri(),),
              subtitle: Text(quran.getSurahName(index + 1)),
              trailing: Text(quran.getVerseCount(index + 1).toString()),
            );
          },
        ),
      ),
    );
  }
}

// ignore: must_be_immutable
class DetailSurah extends StatelessWidget {
  var snum;
  DetailSurah(this.snum, {super.key});

  @override
  Widget build(BuildContext context) {
    return  Scaffold(
        appBar: AppBar(
          title: Text(quran.getSurahName(snum)),
        ),
        body: SafeArea(
          child: Padding(
            padding: EdgeInsets.all(15.0),
            child: ListView.builder(
              itemCount: quran.getVerseCount(snum),
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(
                    quran.getVerse(snum, index + 1, verseEndSymbol: true),
                    textAlign: TextAlign.right,
                    style: GoogleFonts.amiri(),
                  ),
                );
              },
            ),
          ),
        ),
      );
  }
}
