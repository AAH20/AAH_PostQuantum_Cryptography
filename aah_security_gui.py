#!/usr/bin/env python3
"""
AAH Security - GUI Application
Standalone GUI with license checking, key generation, and encryption

Author: Ahmed Hassan (A2Z SOC)
Date: October 3, 2025
"""

import os
import sys
import json
import base64
import hashlib
import hmac
import secrets
import time
import struct
import zlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from typing import Dict, List, Any, Tuple
from tkinter import simpledialog
from aah_pqcore import PQCore

class AAHSecurityGUI:
    """AAH Security GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Superior Post Quantum Asymmetric Cryptography")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Licensing disabled for open-source build
        self.license_valid = True
        
        # Initialize AAH Security
        self.aah = AAHSecurity(use_native=True)
        
        # Create GUI
        self.create_gui()
        
        # Load existing keys
        self.load_keys()
        # Load contacts
        self.load_contacts()
    
    def validate_license(self) -> bool:
        """Licensing disabled in OSS build"""
        return True
    
    def generate_signature(self, data: Dict[str, Any]) -> str:
        """Generate license signature"""
        data_str = json.dumps(data, sort_keys=True)
        key = b'aah_security_license_key_2025'
        signature = hmac.new(key, data_str.encode(), hashlib.sha256).hexdigest()
        return signature
    
    def show_license_error(self):
        """No-op in OSS build"""
        pass
    
    def create_gui(self):
        """Create GUI interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(title_frame, 
                              text="Superior Post Quantum Asymmetric Cryptography",
                              font=('Arial', 16, 'bold'),
                              fg='white',
                              bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Exceeding Intelligence Agency Capabilities",
                                 font=('Arial', 10),
                                 fg='#bdc3c7',
                                 bg='#2c3e50')
        subtitle_label.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Key Management Tab
        self.create_key_management_tab(notebook)
        
        # Encryption Tab
        self.create_encryption_tab(notebook)
        
        # Contacts Tab
        self.create_contacts_tab(notebook)
        
        # Sign/Verify Tab
        self.create_sign_verify_tab(notebook)
        
        # License Tab (informational in OSS build)
        self.create_license_tab(notebook)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, 
                             textvariable=self.status_var,
                             relief=tk.SUNKEN,
                             anchor='w',
                             bg='#34495e',
                             fg='white')
        status_bar.pack(side='bottom', fill='x')
    
    def create_key_management_tab(self, notebook):
        """Create key management tab"""
        key_frame = ttk.Frame(notebook)
        notebook.add(key_frame, text="Key Management")
        
        # Key generation section
        gen_frame = ttk.LabelFrame(key_frame, text="Generate New Keys", padding=10)
        gen_frame.pack(fill='x', padx=10, pady=10)
        
        # Key type selection
        ttk.Label(gen_frame, text="Key Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.key_type_var = tk.StringVar(value="encryption")
        key_type_combo = ttk.Combobox(gen_frame, textvariable=self.key_type_var,
                                     values=["encryption", "signature", "master"])
        key_type_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Key size selection
        ttk.Label(gen_frame, text="Key Size:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.key_size_var = tk.StringVar(value="4096")
        key_size_combo = ttk.Combobox(gen_frame, textvariable=self.key_size_var,
                                     values=["2048", "4096", "8192", "16384"])
        key_size_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Generate button
        gen_button = ttk.Button(gen_frame, text="Generate Keys", command=self.generate_keys)
        gen_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Key display section
        display_frame = ttk.LabelFrame(key_frame, text="Generated Keys", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Key list
        self.key_listbox = tk.Listbox(display_frame, height=10)
        self.key_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Key buttons
        key_button_frame = tk.Frame(display_frame)
        key_button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(key_button_frame, text="View Public Key", command=self.view_public_key).pack(side='left', padx=5)
        ttk.Button(key_button_frame, text="View Private Key", command=self.view_private_key).pack(side='left', padx=5)
        ttk.Button(key_button_frame, text="Export Keys", command=self.export_keys).pack(side='left', padx=5)
        ttk.Button(key_button_frame, text="Delete Key", command=self.delete_key).pack(side='left', padx=5)
        
        # Configure grid weights
        gen_frame.columnconfigure(1, weight=1)
    
    def create_encryption_tab(self, notebook):
        """Create encryption tab"""
        enc_frame = ttk.Frame(notebook)
        notebook.add(enc_frame, text="Encryption/Decryption")
        
        # Message input section
        input_frame = ttk.LabelFrame(enc_frame, text="Message Input", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="Message:").pack(anchor='w')
        self.message_text = scrolledtext.ScrolledText(input_frame, height=5)
        self.message_text.pack(fill='x', pady=5)
        
        # Key selection
        key_frame = tk.Frame(input_frame)
        key_frame.pack(fill='x', pady=5)
        
        ttk.Label(key_frame, text="Select Key:").pack(side='left')
        self.selected_key_var = tk.StringVar()
        self.key_combo = ttk.Combobox(key_frame, textvariable=self.selected_key_var)
        self.key_combo.pack(side='left', fill='x', expand=True, padx=5)
        
        # Encryption buttons
        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt_message).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt_message).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_message).pack(side='left', padx=5)

        # Encrypt to Contact
        contact_frame = ttk.LabelFrame(enc_frame, text="Encrypt to Contact (Public Key)", padding=10)
        contact_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(contact_frame, text="Contact:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_combo = ttk.Combobox(contact_frame, textvariable=self.contact_var)
        self.contact_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        ttk.Button(contact_frame, text="Encrypt To Contact", command=self.encrypt_to_contact).grid(row=0, column=2, padx=5)
        contact_frame.columnconfigure(1, weight=1)
        
        # Result section
        result_frame = ttk.LabelFrame(enc_frame, text="Result", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8)
        self.result_text.pack(fill='both', expand=True)
        
        # Result buttons
        result_button_frame = tk.Frame(result_frame)
        result_button_frame.pack(fill='x', pady=5)
        
        ttk.Button(result_button_frame, text="Copy Result", command=self.copy_result).pack(side='left', padx=5)
        ttk.Button(result_button_frame, text="Save Result", command=self.save_result).pack(side='left', padx=5)
        ttk.Button(result_button_frame, text="Load File", command=self.load_file).pack(side='left', padx=5)

    def create_contacts_tab(self, notebook):
        """Create contacts tab for managing public keys"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Contacts")
        
        list_frame = ttk.LabelFrame(frame, text="Contacts", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.contacts_listbox = tk.Listbox(list_frame, height=10)
        self.contacts_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        btns = tk.Frame(list_frame)
        btns.pack(fill='x', padx=5, pady=5)
        ttk.Button(btns, text="Import Public Key (JSON)", command=self.import_contact).pack(side='left', padx=5)
        ttk.Button(btns, text="Add Manually", command=self.add_contact_manually).pack(side='left', padx=5)
        ttk.Button(btns, text="Export", command=self.export_contact).pack(side='left', padx=5)
        ttk.Button(btns, text="Delete", command=self.delete_contact).pack(side='left', padx=5)

    def create_sign_verify_tab(self, notebook):
        """Create tab for signing and verifying messages"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Sign / Verify")
        
        # Sign section
        sign_frame = ttk.LabelFrame(frame, text="Sign Message (using your key)", padding=10)
        sign_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(sign_frame, text="Select Your Key:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.sign_key_var = tk.StringVar()
        self.sign_key_combo = ttk.Combobox(sign_frame, textvariable=self.sign_key_var)
        self.sign_key_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        ttk.Button(sign_frame, text="Sign Current Message", command=self.sign_current_message).grid(row=0, column=2, padx=5)
        sign_frame.columnconfigure(1, weight=1)
        
        # Verify section
        verify_frame = ttk.LabelFrame(frame, text="Verify Signature (using contact public key)", padding=10)
        verify_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(verify_frame, text="Contact:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.verify_contact_var = tk.StringVar()
        self.verify_contact_combo = ttk.Combobox(verify_frame, textvariable=self.verify_contact_var)
        self.verify_contact_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        ttk.Label(verify_frame, text="Signature:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.signature_entry = ttk.Entry(verify_frame)
        self.signature_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        ttk.Button(verify_frame, text="Verify Current Message", command=self.verify_current_message).grid(row=1, column=2, padx=5)
        verify_frame.columnconfigure(1, weight=1)
    
    def create_license_tab(self, notebook):
        """Create license tab"""
        license_frame = ttk.Frame(notebook)
        notebook.add(license_frame, text="License Information")
        
        # License info
        info_frame = ttk.LabelFrame(license_frame, text="License (OSS Build)", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.license_text = scrolledtext.ScrolledText(info_frame, height=15)
        self.license_text.pack(fill='both', expand=True)
        
        # Load license info
        self.load_license_info()
    
    def load_license_info(self):
        """Load license information"""
        self.license_text.delete('1.0', tk.END)
        self.license_text.insert('1.0', "Licensing is disabled in this open-source build.\nYou can use all features without a license.")
    
    def generate_keys(self):
        """Generate new keys"""
        try:
            key_type = self.key_type_var.get()
            key_size = int(self.key_size_var.get())
            
            # Generate key pair
            private_key, public_key = self.aah.generate_key_pair(key_type, key_size)
            
            # Store keys
            key_id = f"{key_type}_{int(time.time())}"
            self.aah.store_key(key_id, private_key, public_key, key_type, key_size)
            
            # Update UI
            self.load_keys()
            self.status_var.set(f"Generated {key_type} key with {key_size} bits")
            
            messagebox.showinfo("Success", f"Generated {key_type} key successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate keys: {str(e)}")
    
    def load_keys(self):
        """Load existing keys"""
        try:
            keys = self.aah.get_stored_keys()
            self.key_listbox.delete(0, tk.END)
            self.key_combo['values'] = []
            self.sign_key_combo['values'] = []
            
            for key_id, key_info in keys.items():
                display_text = f"{key_id} ({key_info['type']}, {key_info['size']} bits)"
                self.key_listbox.insert(tk.END, display_text)
                self.key_combo['values'] = (*self.key_combo['values'], key_id)
                self.sign_key_combo['values'] = (*self.sign_key_combo['values'], key_id)
            
            if keys:
                self.selected_key_var.set(list(keys.keys())[0])
                self.sign_key_var.set(list(keys.keys())[0])
                
        except Exception as e:
            self.status_var.set(f"Error loading keys: {str(e)}")

    def load_contacts(self):
        """Load contacts into UI"""
        try:
            contacts = self.aah.get_contacts()
            self.contacts_listbox.delete(0, tk.END)
            names = []
            for name in sorted(contacts.keys()):
                self.contacts_listbox.insert(tk.END, name)
                names.append(name)
            self.contact_combo['values'] = tuple(names)
            self.verify_contact_combo['values'] = tuple(names)
            if names:
                self.contact_var.set(names[0])
                self.verify_contact_var.set(names[0])
        except Exception as e:
            self.status_var.set(f"Error loading contacts: {str(e)}")
    
    def view_public_key(self):
        """View public key"""
        try:
            key_id = self.get_selected_key()
            if not key_id:
                return
            
            keys = self.aah.get_stored_keys()
            if key_id in keys:
                public_key = keys[key_id]['public_key']
                self.show_key_dialog("Public Key", public_key)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view public key: {str(e)}")
    
    def view_private_key(self):
        """View private key"""
        try:
            key_id = self.get_selected_key()
            if not key_id:
                return
            
            keys = self.aah.get_stored_keys()
            if key_id in keys:
                private_key = keys[key_id]['private_key']
                self.show_key_dialog("Private Key", private_key)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view private key: {str(e)}")
    
    def show_key_dialog(self, title: str, key: str):
        """Show key in dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("600x400")
        
        text_widget = scrolledtext.ScrolledText(dialog, wrap=tk.WORD)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', key)
        text_widget.config(state='disabled')
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def get_selected_key(self) -> str:
        """Get selected key ID"""
        selection = self.key_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a key!")
            return None
        
        key_text = self.key_listbox.get(selection[0])
        return key_text.split(' ')[0]
    
    def encrypt_message(self):
        """Encrypt message"""
        try:
            message = self.message_text.get('1.0', tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to encrypt!")
                return
            
            key_id = self.selected_key_var.get()
            if not key_id:
                messagebox.showwarning("Warning", "Please select a key!")
                return
            
            # Encrypt message
            encrypted = self.aah.encrypt_message(message, key_id)
            
            # Display result
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', encrypted)
            
            self.status_var.set("Message encrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt message: {str(e)}")
    
    def decrypt_message(self):
        """Decrypt message"""
        try:
            encrypted = self.message_text.get('1.0', tk.END).strip()
            if not encrypted:
                messagebox.showwarning("Warning", "Please enter encrypted message to decrypt!")
                return
            
            key_id = self.selected_key_var.get()
            if not key_id:
                messagebox.showwarning("Warning", "Please select a key!")
                return
            
            # Decrypt message
            decrypted = self.aah.decrypt_message(encrypted, key_id)
            
            # Display result
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', decrypted)
            
            self.status_var.set("Message decrypted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt message: {str(e)}")

    def encrypt_to_contact(self):
        """Encrypt message using selected contact's public key"""
        try:
            message = self.message_text.get('1.0', tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to encrypt!")
                return
            contact_name = self.contact_var.get()
            if not contact_name:
                messagebox.showwarning("Warning", "Please select a contact!")
                return
            encrypted = self.aah.encrypt_for_contact(message, contact_name)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', encrypted)
            self.status_var.set(f"Encrypted for contact '{contact_name}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt to contact: {str(e)}")

    def import_contact(self):
        """Import a contact from JSON file with fields: name, public_key"""
        try:
            path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
            if not path:
                return
            self.aah.import_public_key(path)
            self.load_contacts()
            messagebox.showinfo("Success", "Public key imported")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import public key: {str(e)}")

    def add_contact_manually(self):
        """Prompt for name and public key and add contact"""
        try:
            name = simpledialog.askstring("Add Contact", "Contact name:")
            if not name:
                return
            public_key = simpledialog.askstring("Add Contact", "Public key:")
            if not public_key:
                return
            self.aah.add_contact(name, public_key)
            self.load_contacts()
            messagebox.showinfo("Success", "Contact added")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add contact: {str(e)}")

    def export_contact(self):
        """Export selected contact to JSON"""
        try:
            selection = self.contacts_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a contact to export!")
                return
            name = self.contacts_listbox.get(selection[0])
            path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if not path:
                return
            self.aah.export_contact(name, path)
            messagebox.showinfo("Success", "Contact exported")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export contact: {str(e)}")

    def delete_contact(self):
        """Delete selected contact"""
        try:
            selection = self.contacts_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a contact to delete!")
                return
            name = self.contacts_listbox.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete contact '{name}'?"):
                self.aah.delete_contact(name)
                self.load_contacts()
                self.status_var.set(f"Deleted contact '{name}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete contact: {str(e)}")

    def sign_current_message(self):
        """Sign message using selected local key"""
        try:
            message = self.message_text.get('1.0', tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to sign!")
                return
            key_id = self.sign_key_var.get()
            if not key_id:
                messagebox.showwarning("Warning", "Please select your key!")
                return
            signature = self.aah.sign_message(key_id, message)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', signature)
            self.status_var.set("Message signed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sign message: {str(e)}")

    def verify_current_message(self):
        """Verify signature using selected contact's public key"""
        try:
            message = self.message_text.get('1.0', tk.END).strip()
            if not message:
                messagebox.showwarning("Warning", "Please enter a message to verify!")
                return
            contact_name = self.verify_contact_var.get()
            if not contact_name:
                messagebox.showwarning("Warning", "Please select a contact!")
                return
            signature = self.signature_entry.get().strip()
            if not signature:
                messagebox.showwarning("Warning", "Please enter a signature!")
                return
            ok = self.aah.verify_signature(contact_name, message, signature)
            if ok:
                messagebox.showinfo("Verification", "Signature is valid (demo)")
            else:
                messagebox.showerror("Verification", "Signature is invalid")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to verify signature: {str(e)}")
    
    def clear_message(self):
        """Clear message and result"""
        self.message_text.delete('1.0', tk.END)
        self.result_text.delete('1.0', tk.END)
        self.status_var.set("Cleared")
    
    def copy_result(self):
        """Copy result to clipboard"""
        result = self.result_text.get('1.0', tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_var.set("Result copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No result to copy!")
    
    def save_result(self):
        """Save result to file"""
        result = self.result_text.get('1.0', tk.END).strip()
        if not result:
            messagebox.showwarning("Warning", "No result to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                self.status_var.set(f"Result saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def load_file(self):
        """Load file into message text"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.message_text.delete('1.0', tk.END)
                self.message_text.insert('1.0', content)
                self.status_var.set(f"File loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def export_keys(self):
        """Export keys to file"""
        try:
            key_id = self.get_selected_key()
            if not key_id:
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                self.aah.export_key(key_id, filename)
                self.status_var.set(f"Key exported to {filename}")
                messagebox.showinfo("Success", "Key exported successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export key: {str(e)}")
    
    def delete_key(self):
        """Delete selected key"""
        try:
            key_id = self.get_selected_key()
            if not key_id:
                return
            
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete key '{key_id}'?"):
                self.aah.delete_key(key_id)
                self.load_keys()
                self.status_var.set(f"Key '{key_id}' deleted")
                messagebox.showinfo("Success", "Key deleted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete key: {str(e)}")

class AAHSecurity:
    """AAH Security Core Implementation"""
    
    def __init__(self, use_native=False):
        self.keys_dir = os.path.join(os.path.dirname(__file__), "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.contacts_file = os.path.join(os.path.dirname(__file__), "contacts.json")
        # PQ Core abstraction
        self.pq = PQCore(kem='Kyber1024', sig='Dilithium5', prefer_oqs=not use_native, use_native=use_native)
        self.pq_kem_scheme = 'Kyber1024'  # For compatibility with contacts
    
    def generate_key_pair(self, key_type: str, key_size: int) -> Tuple[str, str]:
        """Generate post-quantum key pairs (Kyber for encryption, Dilithium for signature/master)."""
        if key_type == 'encryption':
            return self.pq.generate_encryption_keys()
        elif key_type in ('signature', 'master'):
            return self.pq.generate_signature_keys()
        else:
            raise ValueError('Unknown key type')
    
    def store_key(self, key_id: str, private_key: str, public_key: str, key_type: str, key_size: int):
        """Store key pair"""
        key_data = {
            'key_id': key_id,
            'private_key': private_key,
            'public_key': public_key,
            'type': key_type,
            'size': key_size,
            'created': time.time()
        }
        
        key_file = os.path.join(self.keys_dir, f"{key_id}.json")
        with open(key_file, 'w') as f:
            json.dump(key_data, f, indent=2)
    
    def get_stored_keys(self) -> Dict[str, Dict[str, Any]]:
        """Get all stored keys"""
        keys = {}
        
        for filename in os.listdir(self.keys_dir):
            if filename.endswith('.json'):
                key_file = os.path.join(self.keys_dir, filename)
                try:
                    with open(key_file, 'r') as f:
                        key_data = json.load(f)
                    keys[key_data['key_id']] = key_data
                except:
                    continue
        
        return keys

    # Contacts management
    def get_contacts(self) -> Dict[str, Dict[str, Any]]:
        if not os.path.exists(self.contacts_file):
            return {}
        try:
            with open(self.contacts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def save_contacts(self, contacts: Dict[str, Dict[str, Any]]):
        with open(self.contacts_file, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2)

    def add_contact(self, name: str, public_key: str):
        """Add a contact with a Kyber public key (base64)."""
        contacts = self.get_contacts()
        contacts[name] = {
            'kem_public_key': public_key,
            'kem_scheme': self.pq_kem_scheme
        }
        self.save_contacts(contacts)

    def delete_contact(self, name: str):
        contacts = self.get_contacts()
        if name in contacts:
            del contacts[name]
            self.save_contacts(contacts)

    def import_public_key(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        name = data.get('name') or data.get('contact') or data.get('label')
        kem_pk = data.get('kem_public_key') or data.get('public_key')
        sig_pk = data.get('sig_public_key')
        kem_scheme = data.get('kem_scheme') or self.pq_kem_scheme
        sig_scheme = data.get('sig_scheme') or self.sig_scheme
        if not name or not kem_pk:
            raise ValueError('JSON must include name and kem_public_key/public_key')
        contacts = self.get_contacts()
        contacts[name] = {
            'kem_public_key': kem_pk,
            'kem_scheme': kem_scheme,
            'sig_public_key': sig_pk,
            'sig_scheme': sig_scheme
        }
        self.save_contacts(contacts)

    def export_contact(self, name: str, path: str):
        contacts = self.get_contacts()
        if name not in contacts:
            raise ValueError('Contact not found')
        info = contacts[name]
        out = {
            'name': name,
            'kem_public_key': info.get('kem_public_key'),
            'kem_scheme': info.get('kem_scheme', self.pq_kem_scheme),
            'sig_public_key': info.get('sig_public_key'),
            'sig_scheme': info.get('sig_scheme', self.sig_scheme)
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)

    # PQC helpers
    def encrypt_for_contact(self, message: str, contact_name: str) -> str:
        contacts = self.get_contacts()
        if contact_name not in contacts:
            raise ValueError('Contact not found')
        info = contacts[contact_name]
        kem_pk_b = base64.b64decode(info['kem_public_key'])
        # Use PQ core abstraction
        return self.pq.encrypt_for_pk(message, info['kem_public_key'])

    def sign_message(self, key_id: str, message: str) -> str:
        keys = self.get_stored_keys()
        if key_id not in keys:
            raise ValueError('Key not found')
        if keys[key_id]['type'] not in ('signature', 'master'):
            raise ValueError('Selected key is not a signature-capable key')
        sk_b64 = keys[key_id]['private_key']
        return self.pq.sign(sk_b64, message)

    def verify_signature(self, contact_name: str, message: str, signature: str) -> bool:
        contacts = self.get_contacts()
        if contact_name not in contacts:
            return False
        info = contacts[contact_name]
        sig_pk_b64 = info.get('sig_public_key')
        if not sig_pk_b64:
            return False
        return self.pq.verify(sig_pk_b64, message, signature)
    
    def encrypt_message(self, message: str, key_id: str) -> str:
        """Encrypt to self using your Kyber public key and AEAD envelope."""
        keys = self.get_stored_keys()
        if key_id not in keys:
            raise ValueError(f"Key '{key_id}' not found")
        if keys[key_id]['type'] != 'encryption':
            raise ValueError('Selected key is not an encryption key')
        return self.pq.encrypt_for_pk(message, keys[key_id]['public_key'])
    
    def decrypt_message(self, encrypted_message: str, key_id: str) -> str:
        keys = self.get_stored_keys()
        if key_id not in keys:
            raise ValueError(f"Key '{key_id}' not found. Please generate a new key first.")
        if keys[key_id]['type'] != 'encryption':
            raise ValueError('Selected key is not an encryption key')
        
        # The decrypt_with_sk method now handles both JSON and compact formats
        try:
            return self.pq.decrypt_with_sk(encrypted_message, keys[key_id]['private_key'])
        except Exception as e:
            # If it's a decryption error, it might be the wrong key or invalid format
            raise ValueError(f'Decryption failed: {str(e)}. Make sure you\'re using the correct key and valid encrypted data.')

    # AEAD handled in PQCore
    
    def export_key(self, key_id: str, filename: str):
        """Export key to file"""
        keys = self.get_stored_keys()
        if key_id not in keys:
            raise ValueError(f"Key '{key_id}' not found")
        
        with open(filename, 'w') as f:
            json.dump(keys[key_id], f, indent=2)
    
    def delete_key(self, key_id: str):
        """Delete key"""
        key_file = os.path.join(self.keys_dir, f"{key_id}.json")
        if os.path.exists(key_file):
            os.remove(key_file)

def main():
    """Main function"""
    root = tk.Tk()
    app = AAHSecurityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
