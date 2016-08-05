//
//  SettingsViewController.swift
//  MobilniToken
//
//  Created by rLoka on 04/08/16.
//  Copyright © 2016 rLoka. All rights reserved.
//

import UIKit

class SettingsViewController: UIViewController {
    
    let defaults = UserDefaults.standard
    
    @IBOutlet weak var tbIpAddress: UITextField!
    @IBOutlet weak var tbPort: UITextField!
    @IBOutlet weak var tbId: UITextField!
    
    @IBAction func btnSaveClick(_ sender: AnyObject) {
        if let text = tbIpAddress.text where !text.isEmpty
        {
            defaults.set(tbIpAddress.text, forKey: "serverIp")
        }
        
        if let text = tbPort.text where !text.isEmpty
        {
            let serverPort: Int? = Int(tbPort.text!)
            defaults.set(serverPort!, forKey: "serverPort")
        }
        
        if let text = tbId.text where !text.isEmpty
        {
            defaults.set(tbId.text, forKey: "userKey")
        }
        
    }
    
    func dismissKeyboard() {
        view.endEditing(true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //Looks for single or multiple taps.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
        
        if let serverIp = defaults.string(forKey: "serverIp") {
            tbIpAddress.text = serverIp
        }
        
        let serverPort = defaults.integer(forKey: "serverPort")
        
        if serverPort != 0{
            tbPort.text = String(serverPort)
        }
        
        if let userKey = defaults.string(forKey: "userKey") {
            tbId.text = userKey
        }
        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
