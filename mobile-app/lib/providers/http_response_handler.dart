import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void httpResponseHander({
  required http.Response response,
  required BuildContext context,
  required VoidCallback onSuccess,
  required VoidCallback onFailiure,
}) {
  switch (response.statusCode) {
    case 200:
      onSuccess();
      break;
    case 201:
      onSuccess();
      break;
    case 204:
      onSuccess();
      break;
    case 400:
      final Map<String, dynamic> body = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(body['message']),
          backgroundColor: Colors.red,
        ),
      );
      onFailiure();
      break;
    case 401:
      final Map<String, dynamic> body = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(body['message']),
          backgroundColor: Colors.red,
        ),
      );
      onFailiure();
      break;

    case 403:
      final Map<String, dynamic> body = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(body['message']),
          backgroundColor: Colors.red,
        ),
      );
      onFailiure();
      break;

    case 404:
      final Map<String, dynamic> body = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(body['message']),
          backgroundColor: Colors.red,
        ),
      );
      onFailiure();
      break;

    case 500:
      final Map<String, dynamic> body = jsonDecode(response.body);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(body['message']),
          backgroundColor: Colors.red,
        ),
      );
      onFailiure();
      break;


  }
}
