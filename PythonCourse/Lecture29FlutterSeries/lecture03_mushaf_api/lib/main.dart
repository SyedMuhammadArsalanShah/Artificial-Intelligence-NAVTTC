import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

void main() {
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
    return MaterialApp(home: SurahIndexSCR());
  }
}

class SurahIndexSCR extends StatefulWidget {
  const SurahIndexSCR({super.key});

  @override
  State<SurahIndexSCR> createState() => _SurahIndexSCRState();
}

class _SurahIndexSCRState extends State<SurahIndexSCR> {
  Map responseMap = {};
  List responseList = [];
  void surahIndexCallKaren() async {
    http.Response response = await http.get(
      Uri.parse("https://api.alquran.cloud/v1/surah"),
    );

    if (response.statusCode == 200) {
      setState(() {
        responseMap = jsonDecode(response.body);
        responseList = responseMap["data"];
      });
    }
  }

  @override
  void initState() {
    // TODO: implement initState

    surahIndexCallKaren();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: responseList.length,
        itemBuilder: (context, index) {
          return ListTile(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => DetailSurah(index + 1)),
              );
            },

            leading: CircleAvatar(child: Text("${index + 1}")),

            title: Text(
              responseList[index]["name"],
              style: GoogleFonts.amiriQuran(),
            ),
            subtitle: Text(responseList[index]["englishName"]),
            trailing: Text(responseList[index]["numberOfAyahs"].toString()),
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
  Map responseMap = {};
  List responseList = [];
  void surahCallKaren() async {
    var surahnumber = widget.surahnum;
    http.Response response = await http.get(
      Uri.parse("https://api.alquran.cloud/v1/surah/$surahnumber"),
    );

    if (response.statusCode == 200) {
      setState(() {
        responseMap = jsonDecode(response.body);
        responseList = responseMap["data"]["ayahs"];
      });
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    surahCallKaren();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: responseList.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(
              responseList[index]["text"],
              textAlign: TextAlign.right,
              style: GoogleFonts.amiriQuran(),
            ),
          );
        },
      ),
    );
  }
}
