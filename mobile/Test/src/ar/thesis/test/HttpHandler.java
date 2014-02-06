package ar.thesis.test;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

public class HttpHandler {

	  public String post(String posturl, List<NameValuePair> params){

		  try {

			  HttpClient httpclient = new DefaultHttpClient();
			  HttpPost httppost = new HttpPost(posturl);
			  httppost.setEntity(new UrlEncodedFormEntity(params));

			  HttpResponse resp = httpclient.execute(httppost);
			  HttpEntity ent = resp.getEntity();

			  String text = EntityUtils.toString(ent);

			  return text;

		  }
		  catch(Exception e) { 
			  return "error";
		  }

		}

	}
