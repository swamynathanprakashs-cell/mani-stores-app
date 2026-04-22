import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Change this to your computer's IP when testing on real device
  // Use 10.0.2.2 for Android Emulator
  static const String baseUrl = 'http://10.0.2.2:8080/api';

  // Get stored JWT token
  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  // Save tokens after login
  static Future<void> saveTokens(String access, String refresh) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', access);
    await prefs.setString('refresh_token', refresh);
  }

  // Clear tokens on logout
  static Future<void> clearTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('refresh_token');
  }

  // Headers with JWT token
  static Future<Map<String, String>> authHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  // ── AUTH ──────────────────────────────────
  static Future<Map<String, dynamic>> signup(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/signup/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }

  static Future<Map<String, dynamic>> login(String phone, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'phone_number': phone, 'password': password}),
    );
    return jsonDecode(response.body);
  }

  // ── PRODUCTS ──────────────────────────────
  static Future<List<dynamic>> getProducts({String? category, String? search}) async {
    String url = '$baseUrl/products/';
    if (category != null) url += '?category=$category';
    if (search != null) url += '?search=$search';

    final response = await http.get(Uri.parse(url));
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getCategories() async {
    final response = await http.get(Uri.parse('$baseUrl/products/categories/'));
    return jsonDecode(response.body);
  }

  // ── ORDERS ────────────────────────────────
  static Future<Map<String, dynamic>> placeOrder(Map<String, dynamic> data) async {
    final headers = await authHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/orders/place/'),
      headers: headers,
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getMyOrders() async {
    final headers = await authHeaders();
    final response = await http.get(
      Uri.parse('$baseUrl/orders/'),
      headers: headers,
    );
    return jsonDecode(response.body);
  }

  // ── PAYMENTS ──────────────────────────────
  static Future<Map<String, dynamic>> recordPayment(Map<String, dynamic> data) async {
    final headers = await authHeaders();
    final response = await http.post(
      Uri.parse('$baseUrl/payments/pay/'),
      headers: headers,
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }

  static Future<List<dynamic>> getTransactionHistory() async {
    final headers = await authHeaders();
    final response = await http.get(
      Uri.parse('$baseUrl/payments/history/'),
      headers: headers,
    );
    return jsonDecode(response.body);
  }
}