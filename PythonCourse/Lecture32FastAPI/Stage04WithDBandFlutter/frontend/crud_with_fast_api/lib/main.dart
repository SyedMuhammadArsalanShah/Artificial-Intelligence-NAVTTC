import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "FastAPI CRUD",
      theme: ThemeData(
        brightness: Brightness.light,
        primarySwatch: Colors.indigo,
        scaffoldBackgroundColor: Color(0xFFF5F6FA),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          labelStyle:
              TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide.none,
          ),
        ),
      ),
      debugShowCheckedModeBanner: false,
      home: ItemScreen(),
    );
  }
}

class ItemScreen extends StatefulWidget {
  @override
  State<ItemScreen> createState() => _ItemScreenState();
}

class _ItemScreenState extends State<ItemScreen> {
  String api = "http://127.0.0.1:8000/items";
  List items = [];
  bool loading = false;

  final nameCtrl = TextEditingController();
  final priceCtrl = TextEditingController();

  Future fetchItems() async {
    setState(() => loading = true);
    final res = await http.get(Uri.parse(api));
    items = jsonDecode(res.body);
    setState(() => loading = false);
  }

  Future addItem() async {
    if (nameCtrl.text.isEmpty || priceCtrl.text.isEmpty) return;

    await http.post(
      Uri.parse(api),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "name": nameCtrl.text.trim(),
        "price": double.parse(priceCtrl.text),
      }),
    );

    nameCtrl.clear();
    priceCtrl.clear();
    fetchItems();
  }

  Future deleteItem(String id) async {
    await http.delete(Uri.parse("$api/$id"));
    fetchItems();
  }

  /// ============================
  ///      UPDATE ITEM
  /// ============================
  Future updateItem(String id, String name, double price) async {
    await http.put(
      Uri.parse("$api/$id"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "name": name,
        "price": price,
      }),
    );
    fetchItems();
  }

  /// SHOW UPDATE BOTTOMSHEET
  void showUpdateSheet(String id, String oldName, double oldPrice) {
    final updateName = TextEditingController(text: oldName);
    final updatePrice = TextEditingController(text: oldPrice.toString());

    showModalBottomSheet(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
      ),
      context: context,
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                "Update Item",
                style: TextStyle(
                    fontSize: 20, fontWeight: FontWeight.bold),
              ),

              SizedBox(height: 15),

              TextField(
                controller: updateName,
                decoration: InputDecoration(
                  labelText: "Item Name",
                  prefixIcon: Icon(Icons.edit),
                ),
              ),

              SizedBox(height: 12),

              TextField(
                controller: updatePrice,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: "Price",
                  prefixIcon: Icon(Icons.numbers),
                ),
              ),

              SizedBox(height: 20),

              ElevatedButton.icon(
                icon: Icon(Icons.save),
                label: Text("Save Changes"),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16)),
                ),
                onPressed: () {
                  updateItem(
                    id,
                    updateName.text,
                    double.parse(updatePrice.text),
                  );
                  Navigator.pop(context);
                },
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  void initState() {
    fetchItems();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "FastAPI + Flutter",
          style: TextStyle(fontWeight: FontWeight.w600),
        ),
        elevation: 3,
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // GLASS CARD INPUT FORM
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.9),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 20,
                    offset: Offset(0, 10),
                  ),
                ],
              ),
              child: Column(
                children: [
                  TextField(
                    controller: nameCtrl,
                    decoration: InputDecoration(
                      labelText: "Item Name",
                      prefixIcon: Icon(Icons.shopping_bag_outlined),
                    ),
                  ),

                  SizedBox(height: 12),

                  TextField(
                    controller: priceCtrl,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: "Price",
                      prefixIcon: Icon(Icons.numbers),
                    ),
                  ),

                  SizedBox(height: 14),

                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      padding: EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16)),
                    ),
                    icon: Icon(Icons.add),
                    label: Text("Add Item", style: TextStyle(fontSize: 16)),
                    onPressed: addItem,
                  ),
                ],
              ),
            ),

            SizedBox(height: 20),

            Expanded(
              child: loading
                  ? Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      itemCount: items.length,
                      itemBuilder: (context, i) {
                        final item = items[i];

                        return Card(
                          elevation: 4,
                          margin: EdgeInsets.only(bottom: 14),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: ListTile(
                            contentPadding: EdgeInsets.all(16),
                            title: Text(
                              item["name"],
                              style: TextStyle(
                                  fontWeight: FontWeight.w600, fontSize: 17),
                            ),
                            subtitle: Text(
                              "Rs ${item["price"]}",
                              style: TextStyle(
                                  fontSize: 14, color: Colors.grey),
                            ),

                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                // EDIT BUTTON
                                IconButton(
                                  icon: Icon(Icons.edit, color: Colors.blue),
                                  onPressed: () {
                                    showUpdateSheet(
                                      item["id"].toString(),
                                      item["name"],
                                      double.parse(item["price"].toString()),
                                    );
                                  },
                                ),

                                // DELETE BUTTON
                                IconButton(
                                  icon: Icon(Icons.delete, color: Colors.red),
                                  onPressed: () =>
                                      deleteItem(item["id"].toString()),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
