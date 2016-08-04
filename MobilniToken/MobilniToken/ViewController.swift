//
//  ViewController.swift
//  MobilniToken
//
//  Created by rLoka on 03/08/16.
//  Copyright © 2016 rLoka. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    //Alerts
    let alertController = UIAlertController(title: "Postavke", message: "Molimo, popunite sve vrijednosti u Postavkama prije korištenja!", preferredStyle: UIAlertControllerStyle.alert)
    
    //Identifikacijski podaci uređaja/tokena
    let gDeviceKey = UIDevice.current().identifierForVendor!.uuidString
    var gUserKey: String?
     
    //SuperGlobalna varijabla za spremanje postavki
    let defaults = UserDefaults.standard
    
    //Da li su sve postavke učitane?
    var isEverythingSet = false
    
    //Socket
    var client: TCPClient!
    
    func approveToken(token: String){
        let refreshAlert = UIAlertController(title: token, message: "Da li želite potvrditi sljedeću transakciju?.", preferredStyle: UIAlertControllerStyle.alert)
        
        refreshAlert.addAction(UIAlertAction(title: "Da", style: .default, handler: { (action: UIAlertAction!) in
            self.client.send(str: "ok:" + token)
        }))
        
        refreshAlert.addAction(UIAlertAction(title: "Ne", style: .cancel, handler: { (action: UIAlertAction!) in
            self.client.send(str: "no:" + token)
        }))
        
        present(refreshAlert, animated: true, completion: nil)
    }
    
    
    //Spajanje i slanje podataka
    func connectToServer(){
        var (success, _) = client.connect(timeout: 10)
        if !success {
            imageContainer.image = UIImage(named: "multiply-icon")
            lbStatusLabel.text = "Greška pri spajanju"
        }
    }
    
    //Slanje inicijalnog paketa i primanje poeukw
    func sendInitialPackage(){
        self.client.send(str:"key:" + gUserKey! + ";" + gDeviceKey)
        let data = client.read(expectlen: 1024*10)
        if let d = data {
            if let str = NSString(bytes:d, length: d.count, encoding: String.Encoding.utf8.rawValue) as? String{
                print("Primljeno: " + str)
                let keyAndMessage = str.characters.split{$0 == ":"}.map(String.init)
                if (keyAndMessage[0] as? String) != nil {
                    switch keyAndMessage[0] {
                    case "token":
                        approveToken(token: keyAndMessage[1])
                    case "idle":
                        print("idle")
                    case "error":
                        print("error")
                    default:
                        print("default")
                    }
                }
                lbStatusLabel.text = keyAndMessage[1] as String
                imageContainer.image = UIImage(named: "refresh-4-icon")
            }
        }
    }
    
    @IBOutlet weak var lbStatusLabel: UITextField!
    @IBOutlet weak var imageContainer: UIImageView!
    
    @IBOutlet weak var refreshIndicator: UIActivityIndicatorView!
    
    @IBAction func btnRefreshClick(_ sender: AnyObject) {
        if isEverythingSet {
            refreshIndicator.startAnimating()
            sendInitialPackage()
            refreshIndicator.stopAnimating()
        } else {
            present(alertController, animated: true, completion: nil)
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        imageContainer.image = UIImage(named: "check-icon")
        alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default,handler: nil))
        
        if let serverIp = defaults.string(forKey: "serverIp") {
            let serverPort = defaults.integer(forKey: "serverPort")
            
            if serverPort != 0{
                if let userKey = defaults.string(forKey: "userKey") {
                    isEverythingSet = true
                    client = TCPClient(addr: serverIp, port: serverPort)
                    connectToServer()
                    gUserKey = userKey
                }
                else{
                    present(alertController, animated: true, completion: nil)
                }
            }
            else{
                present(alertController, animated: true, completion: nil)
            }
        }
        else{
            present(alertController, animated: true, completion: nil)
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
}

