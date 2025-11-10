void main(List<String> args) {
  String name = "Zaid";
  String email = "l@gmaiil.com";
  String password = "1234";
  String contact = "021";

  print("Account Successfully created");

  String emailLogin = "l@gmaiil.com";
  String passwordLogin = "1234";

  if (email == emailLogin && password == passwordLogin) {
    print("Welcome in Our Class $name");

    num eng, urdu, math, per, obatined;

    eng = 30;
    urdu = 39;
    math = 67;

    obatined = eng + urdu + math;

    per = (obatined / 300) * 100;

    if (per <= 100 && per >= 80) {
      print("Grade A1");
    } else if (per <= 79 && per >= 70) {
      print("Grade A");
    } else if (per <= 69 && per >= 60) {
      print("Grade B");
    } else if (per <= 59 && per >= 50) {
      print("Grade C");
    } else if (per <= 49 && per >= 40) {
      print("Grade F Mehnat Karen");
    } else {
      print("Ghar Bethen Jinaab ");
    }
  } else {
    print("Incorrect Email And Password ");
  }
}
