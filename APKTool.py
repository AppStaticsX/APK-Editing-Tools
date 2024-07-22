import os
import io
import re
import zipfile
import shutil
import subprocess
import webbrowser
import base64
import threading
import customtkinter as ctk
from customtkinter import filedialog
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image

DEFAULT_FONT_STYLE = ("Lucida Handwriting", 14, "bold")
CHECK_FONT_STYLE = ("Lucida Handwriting", 13, "bold")
OUTPUT_TEXT = ("Courier Prime", 11, "bold")
ENTRY_FONT_STYLE = ("Lucida Handwriting", 15, "bold")
APP_LABLE_FONT_STYLE = ("Berlin Sans FB", 16, "bold")

BTN_COLOR = "#FFFFFF"
BTN_TEXT_COLOR = "#000000"

formats = ["BASE64", "JAVA", "HEX"]
output_formats = [".TXT", ".JAVA", ".HEX"]
unique_signature = "aHR0cHM6Ly9naXRodWIuY29tL0FwcFN0YXRpY3NY"
functions_apk = ["VERIFY SIGNATURE", "SIGN APK", "REFACT RESOURCE", "PROTECT APK", "KILL SIGNATURE", "MANIFEST OPERATIONS", "DECOMPILE APK", "COMPILE PROJECT", "CRC32 RESTORE", "REPLACE APK CONTENT", "DEX2SMALI", "SMALI2DEX", "ARSC OPERATIONS"]
functions_apks = ["MERGE BUNDLE"]
kill_options = ["ADD ORIGIN APK", "DON'T ADD"]
protect_options = ["DEX", "RESOURCES"]
decom_options = ["DEX FILES", "RESOURCES"]
com_options = ["AAPT2", "AAPT"]
manifest_options = ["DECODE", "ENCODE"]
sign_option = ["ZIPALIGN", "SKIP ZIPALIGN"]
anti_option = ["OBFUSCATE", "DON'T OBFUSCATE"]
dex_decompile_option = ["MANUAL"]#Automatic option not available yet...
dex_list = ["classes.dex"]
smali_list = ["Select Folder"]
arsc_options = ["DUMP", "COMPILE"]

ctk.set_appearance_mode("DARK")

logo_img = CTkImage(Image.open("ImageResources\\android.png"), size=(30, 30))
btn_image = CTkImage(Image.open("ImageResources\\file_icon.png"), size=(30, 30))
default_icon = CTkImage(Image.open("ImageResources\\android.png"), size=(60, 60))
sublime_icon_disable = CTkImage(Image.open("ImageResources\\subl_dis.png"), size=(28, 28))
sublime_icon_enable = CTkImage(Image.open("ImageResources\\subl_ena.png"), size=(28, 28))
arsc_logo = CTkImage(Image.open("ImageResources\\arsc.png"), size=(28, 28))
copy_img = CTkImage(Image.open("ImageResources\\copy_btn.png"), size=(20, 20))
search_img = CTkImage(Image.open("ImageResources\\search_btn.png"), size=(20, 20))



class APKToolGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("400x540")
        self.window.resizable(False, False)
        self.window.title("AppStaticsX™-APK Editing Tools")
        self.window.iconbitmap(r'ImageResources\\icon.ico')

        self.frame_top = ctk.CTkFrame(self.window, fg_color="transparent")
        self.frame_top.pack()

        self.frame_application = ctk.CTkFrame(self.frame_top, fg_color="transparent")
        self.frame_application.pack(pady=10)

        self.application_logo_label = ctk.CTkButton(self.frame_application, image=logo_img, fg_color="transparent", text="", bg_color="transparent", width=30, height=30, hover="none", command=self.encode_apk_signature)
        self.application_logo_label.pack(side="left", padx=5)

        self.application_name_lable = ctk.CTkLabel(self.frame_application, fg_color="transparent", text="APK EDITING TOOLS", font=APP_LABLE_FONT_STYLE, bg_color="transparent")
        self.application_name_lable.pack(side="right", padx=0)

        self.apk_handle_frame = ctk.CTkFrame(self.window, height=100, width=400, fg_color="transparent")
        self.apk_handle_frame.pack(pady=5)

        self.apk_entry = ctk.CTkEntry(self.apk_handle_frame, width=210, font=CHECK_FONT_STYLE)
        self.apk_entry.pack(side="left", padx=15)

        self.apk_picker_btn = ctk.CTkButton(self.apk_handle_frame, text="", font=DEFAULT_FONT_STYLE, width=30, image=btn_image, fg_color="transparent", hover="none", command=self.browse_apk)
        self.apk_picker_btn.pack(side="right", padx=8)

        self.apk_info_button = ctk.CTkButton(self.apk_handle_frame, text="APK INFO", font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR,text_color=BTN_TEXT_COLOR,state="disabled", hover_color="#0E8849", width=60, command=self.extract_application_info)
        self.apk_info_button.pack(side="left")

        self.apk_function_handle_frame = ctk.CTkFrame(self.window, height=100, width=400, fg_color="transparent")
        self.apk_function_handle_frame.pack(pady=5)

        self.apk_function_reset_btn = ctk.CTkButton(self.apk_function_handle_frame, fg_color=BTN_COLOR, text="DEL", font=ENTRY_FONT_STYLE, text_color=BTN_TEXT_COLOR, width=55, hover_color="#FF0000", command=self.reset_selected_funtion, state="disabled")
        self.apk_function_reset_btn.pack(side="right", padx=10)

        self.apk_function_confirm_btn = ctk.CTkButton(self.apk_function_handle_frame, fg_color=BTN_COLOR, text="GO", font=ENTRY_FONT_STYLE, text_color=BTN_TEXT_COLOR, width=40, hover_color="#0E8849", command=self.update_function, state="disabled")
        self.apk_function_confirm_btn.pack(side="right", padx=5)

        self.apk_function_dropdown = ctk.CTkComboBox(self.apk_function_handle_frame, width=245, values=functions_apk, font=DEFAULT_FONT_STYLE, dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.apk_function_dropdown.pack(side="left", padx=10)

        self.apk_detail_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.apk_detail_frame.pack(pady=10)

        self.apk_logo_lable = ctk.CTkLabel(self.apk_detail_frame, image=default_icon, fg_color="transparent", text="", bg_color="transparent")
        self.apk_logo_lable.pack(side="left", padx=5)

        self.apk_detail_extra_frame = ctk.CTkFrame(self.apk_detail_frame, fg_color="#1d1e1e")
        self.apk_detail_extra_frame.pack(side="right")

        self.apk_detail_copy_btn = ctk.CTkButton(self.apk_detail_extra_frame, text="", font=DEFAULT_FONT_STYLE, width=0, image=copy_img, fg_color="transparent", hover="none", state="disabled", command=self.copy_content)
        self.apk_detail_copy_btn.pack(pady=5, ipadx=0, ipady=0)

        self.apk_explore_btn = ctk.CTkButton(self.apk_detail_extra_frame, text="", font=DEFAULT_FONT_STYLE, width=0, image=search_img, fg_color="transparent", hover="none", state="disabled", command=self.explore_apk)
        self.apk_explore_btn.pack(pady=5, ipadx=0, ipady=0)

        self.apk_detail_output_textbox = ctk.CTkTextbox(self.apk_detail_frame, height=80, width=260, font=OUTPUT_TEXT, wrap="none")
        self.apk_detail_output_textbox.pack(side="right", padx=5)

        self.section_divider_frame = ctk.CTkFrame(self.window, height=5, width=400)
        self.section_divider_frame.pack(pady=5)

        #SigntureVerify_frame_design
        self.signature_verify_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.signature_verify_frame.pack(pady=0)

        self.signature_verify_frame_sub = ctk.CTkFrame(self.signature_verify_frame, fg_color="transparent")
        self.signature_verify_frame_sub.pack(pady=10)

        self.signature_verify_frame_sub_sub = ctk.CTkFrame(self.signature_verify_frame, fg_color="transparent")
        self.signature_verify_frame_sub_sub.pack(pady=0)

        self.signature_verify_format_option_lable = ctk.CTkLabel(self.signature_verify_frame_sub, text="SELECT SIGNATURE VERIFIVATION \nFORMAT(S) FOR EXTRACTION:", font=("Lucida Handwriting", 8, "bold"))
        self.signature_verify_format_option_lable.pack(side="left", padx=10)

        self.signature_verify_format_option_dropdown = ctk.CTkComboBox(self.signature_verify_frame_sub, values=formats, width=130, font=CHECK_FONT_STYLE, dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.signature_verify_format_option_dropdown.pack(side="right", padx=17)
        
        self.signature_verify_output_format_option_lable = ctk.CTkLabel(self.signature_verify_frame_sub_sub, text="SELECT OUTPUT FILE EXTENTION(S)\nFOR EXTRACTION:", font=("Lucida Handwriting", 8, "bold"))
        self.signature_verify_output_format_option_lable.pack(side="left", padx=10)

        self.signature_verify_output_format_option_dropdown = ctk.CTkComboBox(self.signature_verify_frame_sub_sub, values=output_formats, width=130, font=CHECK_FONT_STYLE, dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.signature_verify_output_format_option_dropdown.pack(side="right", padx=10)

        self.run_button_default = ctk.CTkButton(self.signature_verify_frame, text="VERIFY X.509 OF APK", font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.run_button_default.pack(pady=10)

        self.output_default_textbox = ctk.CTkTextbox(self.signature_verify_frame, height=132, width=360, font=OUTPUT_TEXT)
        self.output_default_textbox.pack(pady=10)

        self.other_function_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.other_function_frame.pack_forget()

        #Refact_frame_design
        self.refact_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=200, width=360, font=OUTPUT_TEXT, wrap="none")
        self.refact_output_textbox.pack_forget()

        self.run_btn_frame = ctk.CTkFrame(self.other_function_frame, fg_color="transparent")
        self.run_btn_frame.pack()

        self.run_button_other = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.run_button_other.pack_forget()

        #AntiSplit_protect_frame
        self.antisplit_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.antisplit_frame.pack_forget()

        self.antisplit_option_lable = ctk.CTkLabel(self.antisplit_frame, text="OBFUSCATE RESOURCES WHILE\nMERGE APK BUNDLE:", font=("Lucida Handwriting", 8, "bold"))
        self.antisplit_option_lable.pack_forget()

        self.antisplit_option_dropdown = ctk.CTkComboBox(self.antisplit_frame, values=anti_option, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.antisplit_option_dropdown.pack_forget()

        self.antisplit_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=175, width=360, font=OUTPUT_TEXT, wrap="none")
        self.antisplit_output_textbox.pack_forget()

        #ApkProtect_frame_design
        self.protect_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.protect_frame.pack_forget()

        self.protect_option_lable = ctk.CTkLabel(self.protect_frame, text="SELECT PROTECT FILE TYPE\nDEX OR RESOURCES:", font=("Lucida Handwriting", 8, "bold"))
        self.protect_option_lable.pack_forget()

        self.protect_option_dropdown = ctk.CTkComboBox(self.protect_frame, values=protect_options, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.protect_option_dropdown.pack_forget()

        self.protect_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="PROTECT APK DEX/RESOURCE", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.protect_run_btn.pack_forget()

        self.protect_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.protect_output_textbox.pack_forget()

        #SignatureKill_frame_design
        self.signaturekill_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.signaturekill_frame.pack_forget()

        self.signaturekill_option_lable = ctk.CTkLabel(self.signaturekill_frame, text="ADD ORIGINAL APK TO\nCHECK INTEGRITY:", font=("Lucida Handwriting", 8, "bold"))
        self.signaturekill_option_lable.pack_forget()

        self.signaturekill_option_dropdown = ctk.CTkComboBox(self.signaturekill_frame, width=170, values=kill_options, font=CHECK_FONT_STYLE, dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.signaturekill_option_dropdown.pack_forget()

        self.signaturekill_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.signaturekill_run_btn.pack_forget()

        self.signaturekill_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=165, width=360, font=OUTPUT_TEXT, wrap="none")
        self.signaturekill_output_textbox.pack_forget()

        #Manifest_operation_frame_design
        self.manifest_operation_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.manifest_operation_frame.pack_forget()

        self.manifest_operation_option_lable = ctk.CTkLabel(self.manifest_operation_frame, text="SELECT ANDROID MANIFEST OPTION\nENCODE/DECODE:", font=("Lucida Handwriting", 8, "bold"))
        self.manifest_operation_option_lable.pack_forget()

        self.manifest_operation_option_dropdown = ctk.CTkComboBox(self.manifest_operation_frame, values=manifest_options, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.manifest_operation_option_dropdown.pack_forget()

        self.manifest_operation_run_btn_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.manifest_operation_run_btn_frame.pack_forget()

        self.manifest_operation_run_btn = ctk.CTkButton(self.manifest_operation_run_btn_frame, font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread, text="CLONE APK FILE")
        self.manifest_operation_run_btn.pack_forget()

        self.manifest_operation_sublime_btn = ctk.CTkButton(self.manifest_operation_run_btn_frame, image=sublime_icon_disable, fg_color="transparent", text="", state="disabled", hover="none", command=self.open_sublime, width=24, height=24)
        self.manifest_operation_sublime_btn.pack_forget()

        self.manifest_operation_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.manifest_operation_output_textbox.pack_forget()

        #sign_frame_design
        self.sign_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.sign_frame.pack_forget()

        self.sign_option_lable = ctk.CTkLabel(self.sign_frame, text="ZIPALIGN APK WITH SIGNING\n(ZIPALIGN RECOMMENDED):", font=("Lucida Handwriting", 8, "bold"))
        self.sign_option_lable.pack_forget()

        self.sign_option_dropdown = ctk.CTkComboBox(self.sign_frame, values=sign_option, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.sign_option_dropdown.pack_forget()

        self.sign_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="SIGN APK FILE", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.sign_run_btn.pack_forget()

        self.sign_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.sign_output_textbox.pack_forget()

        #Dex_2_smali_frame_design
        self.dex2smali_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.dex2smali_frame.pack_forget()

        self.dex2smali_frame_sub = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.dex2smali_frame_sub.pack_forget()

        self.dex2smali_option_lable = ctk.CTkLabel(self.dex2smali_frame, text="SELECT DEX FILE DECOMPILE\nMETHOD:  ", font=("Lucida Handwriting", 8, "bold"))
        self.dex2smali_option_lable.pack_forget()

        self.dex2smali_option_dropdown = ctk.CTkComboBox(self.dex2smali_frame, values=dex_decompile_option, font=CHECK_FONT_STYLE, width=180,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.dex2smali_option_dropdown.pack_forget()

        self.dex2smali_manual_option_lable = ctk.CTkLabel(self.dex2smali_frame_sub, text="SELECT DEX FILE WANT TO   \nDECOMPILE:", font=("Lucida Handwriting", 8, "bold"))
        self.dex2smali_manual_option_lable.pack_forget()

        self.dex2smali_dex_name_entry = ctk.CTkComboBox(self.dex2smali_frame_sub, values=dex_list, font=CHECK_FONT_STYLE, width=180,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.dex2smali_dex_name_entry.pack_forget()

        self.dex2smali_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="DECOMPILE DEX FILE", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.dex2smali_run_btn.pack_forget()

        self.dex2smali_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.dex2smali_output_textbox.pack_forget()

        #Smali_2_dex_frame_design
        self.smali2dex_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.smali2dex_frame.pack_forget()

        self.smali2dex_frame_sub = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.smali2dex_frame_sub.pack_forget()

        self.smali2dex_option_lable = ctk.CTkLabel(self.smali2dex_frame, text="SELECT SMALI FILE(s) \nCOMPILE METHOD:  ", font=("Lucida Handwriting", 8, "bold"))
        self.smali2dex_option_lable.pack_forget()

        self.smali2dex_option_dropdown = ctk.CTkComboBox(self.smali2dex_frame, values=dex_decompile_option, font=CHECK_FONT_STYLE, width=180,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.smali2dex_option_dropdown.pack_forget()

        self.smali2dex_manual_option_lable = ctk.CTkLabel(self.smali2dex_frame_sub, text="SELECT SMALI FOLDER\nTO COMPILE:", font=("Lucida Handwriting", 8, "bold"))
        self.smali2dex_manual_option_lable.pack_forget()

        self.smali2dex_smali_name_entry = ctk.CTkComboBox(self.smali2dex_frame_sub, values=smali_list, font=CHECK_FONT_STYLE, width=180,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.smali2dex_smali_name_entry.pack_forget()

        self.smali2dex_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="COMPILE SMALI TO DEX", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.smali2dex_run_btn.pack_forget()

        self.smali2dex_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.smali2dex_output_textbox.pack_forget()

        #CRC32_restore_frame_design
        self.crc32_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.crc32_frame.pack_forget()

        self.crc32_option_lable = ctk.CTkLabel(self.crc32_frame, text="SELECT ORIGINAL/UNTOUCHED APK FOR EXTRACT ENTRIES FOR PATCH", font=("Lucida Handwriting", 8, "bold"))
        self.crc32_option_lable.pack_forget()

        self.crc32_frame_sub = ctk.CTkFrame(self.crc32_frame, fg_color="transparent")
        self.crc32_frame_sub.pack_forget()

        self.crc32_original_apk_entry = ctk.CTkEntry(self.crc32_frame_sub, width=190, font=CHECK_FONT_STYLE)
        self.crc32_original_apk_entry.pack_forget()

        self.crc32_original_apk_pick_btn = ctk.CTkButton(self.crc32_frame_sub, text="PICK ORIGINAL", font=DEFAULT_FONT_STYLE, text_color=BTN_TEXT_COLOR, fg_color=BTN_COLOR, hover="none", command=self.browse_original_apk)
        self.crc32_original_apk_pick_btn.pack_forget()

        self.crc32_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="RESTORE CRC32 CHECKSUM", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.crc32_run_btn.pack_forget()

        self.crc32_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=165, width=360, font=OUTPUT_TEXT, wrap="none")
        self.crc32_output_textbox.pack_forget()

        #Replace_content_frame_design
        self.replace_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.replace_frame.pack_forget()

        self.replace_frame_sub = ctk.CTkFrame(self.replace_frame, fg_color="transparent")
        self.replace_frame_sub.pack_forget()

        self.replace_content_entry = ctk.CTkEntry(self.replace_frame_sub, width=200, font=CHECK_FONT_STYLE)
        self.replace_content_entry.pack_forget()

        self.replace_content_pick_btn = ctk.CTkButton(self.replace_frame_sub, text="PICK A FILE", font=DEFAULT_FONT_STYLE, text_color=BTN_TEXT_COLOR, fg_color=BTN_COLOR, hover="none", command=self.browse_replacement_file)
        self.replace_content_pick_btn.pack_forget()

        self.replace_run_btn = ctk.CTkButton(self.run_btn_frame, font=DEFAULT_FONT_STYLE, text="REPLACE WITH SELECTED FILE", fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.replace_run_btn.pack_forget()

        self.replace_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=180, width=360, font=OUTPUT_TEXT, wrap="none")
        self.replace_output_textbox.pack_forget()

        #Decompile_&_compile_frame_design
        self.compile_decompile_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.compile_decompile_frame.pack_forget()

        self.decompile_option_lable = ctk.CTkLabel(self.compile_decompile_frame, text="CHOOSE WHICH APK PART\nTO DECOMPILE:", font=("Lucida Handwriting", 8, "bold"))
        self.decompile_option_lable.pack_forget()

        self.decompile_option_dropdown = ctk.CTkComboBox(self.compile_decompile_frame, values=decom_options, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.decompile_option_dropdown.pack_forget()

        self.compile_option_lable = ctk.CTkLabel(self.compile_decompile_frame, text="SELECT ANDROID ASSEST PACKAGING\nTOOL VERSION:", font=("Lucida Handwriting", 8, "bold"))
        self.compile_option_lable.pack_forget()

        self.compile_option_dropdown = ctk.CTkComboBox(self.compile_decompile_frame, values=com_options, font=CHECK_FONT_STYLE, width=125,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.compile_option_dropdown.pack_forget()

        self.compile_decompile_run_btn_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.compile_decompile_run_btn_frame.pack_forget()

        self.compile_decompile_run_btn = ctk.CTkButton(self.compile_decompile_run_btn_frame, font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.compile_decompile_run_btn.pack_forget()

        self.compile_decompile_sublime_btn = ctk.CTkButton(self.compile_decompile_run_btn_frame, image=sublime_icon_disable, fg_color="transparent", text="", state="disabled", hover="none", command=self.open_sublime, width=24, height=24)
        self.compile_decompile_sublime_btn.pack_forget()

        self.decompile_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.decompile_output_textbox.pack_forget()

        self.compile_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.compile_output_textbox.pack_forget()

        #ARSC_dump_frame_design
        self.arsc_tool_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.arsc_tool_frame.pack_forget()

        self.arsc_tool_option_lable = ctk.CTkLabel(self.arsc_tool_frame, text="SELECT ARSC OPERATION DUMP\nOR RECOMPILE:", font=("Lucida Handwriting", 8, "bold"))
        self.arsc_tool_option_lable.pack_forget()

        self.arsc_tool_option_dropdown = ctk.CTkComboBox(self.arsc_tool_frame, values=arsc_options, font=CHECK_FONT_STYLE, width=150,  dropdown_font=CHECK_FONT_STYLE, dropdown_hover_color="#111111")
        self.arsc_tool_option_dropdown.pack_forget()

        self.arsc_tool_run_btn_frame = ctk.CTkFrame(self.run_btn_frame, fg_color="transparent")
        self.arsc_tool_run_btn_frame.pack_forget()

        self.arsc_tool_run_btn = ctk.CTkButton(self.arsc_tool_run_btn_frame, font=DEFAULT_FONT_STYLE, fg_color=BTN_COLOR, text_color=BTN_TEXT_COLOR, state="disabled", hover_color="#0E8849", width=360, command=self.execution_on_thread)
        self.arsc_tool_run_btn.pack_forget()

        self.arsc_tool_editor_btn = ctk.CTkButton(self.arsc_tool_run_btn_frame, image=arsc_logo, fg_color="transparent", text="", state="disabled", hover="none", command=self.open_arsceditor, width=24, height=24)
        self.arsc_tool_editor_btn.pack_forget()

        self.arsc_tool_sublime_btn = ctk.CTkButton(self.arsc_tool_run_btn_frame, image=sublime_icon_disable, fg_color="transparent", text="", state="disabled", hover="none", command=self.open_sublime, width=24, height=24)
        self.arsc_tool_sublime_btn.pack_forget()

        self.arsc_tool_output_textbox = ctk.CTkTextbox(self.other_function_frame, height=170, width=360, font=OUTPUT_TEXT, wrap="none")
        self.arsc_tool_output_textbox.pack_forget()



    def update_function(self):
       if self.apk_function_dropdown.get() == "MERGE BUNDLE":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack()
            self.antisplit_option_lable.pack(side="left", padx=10)
            self.antisplit_option_dropdown.pack(side="right", padx=10)
            self.run_button_other.pack(pady=20)
            self.run_button_other.configure(state="normal",text="MERGE BUNDLE APK")
            self.antisplit_output_textbox.pack()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "VERIFY SIGNATURE":
            self.signature_verify_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_default.pack(pady=10)
            self.output_default_textbox.pack(pady=10)
            self.other_function_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.run_button_default.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()
        
       elif self.apk_function_dropdown.get() == "SIGN APK":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.sign_output_textbox.pack(pady=10)
            self.protect_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack()
            self.sign_option_lable.pack(side="left", padx=20)
            self.sign_option_dropdown.pack(side="right", padx=20, pady=10)
            self.sign_run_btn.pack(pady=10)
            self.sign_run_btn.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "REFACT RESOURCE":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack(pady=20)
            self.antisplit_frame.pack_forget()
            self.run_button_other.configure(text="REFACT OBFAUSCATED RESOURCES")
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.run_button_other.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "PROTECT APK":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack(pady=10)
            self.sign_output_textbox.pack_forget()
            self.antisplit_frame.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_frame.pack()
            self.protect_run_btn.pack(pady=10)
            self.protect_option_lable.pack(side="left", padx=10)
            self.protect_option_dropdown.pack(side="right", padx=10, pady=10)
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.protect_run_btn.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "KILL SIGNATURE":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.signaturekill_run_btn.configure(text="KILL APPLICATION SIGNATURE")
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack(pady=10)
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_frame.pack()
            self.signaturekill_option_lable.pack(side="left", padx=20)
            self.signaturekill_option_dropdown.pack(side="right", padx=20, pady=10)
            self.signaturekill_run_btn.pack(pady=10)
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.signaturekill_run_btn.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "MANIFEST OPERATIONS":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_frame.pack_forget()
            self.manifest_operation_run_btn.configure(text="DECODE/ENCODE MANIFEST", width=320)
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack(pady=10)
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack()
            self.manifest_operation_option_lable.pack(side="left", padx=10)
            self.manifest_operation_option_dropdown.pack(side="right", padx=10, pady=10)
            self.manifest_operation_run_btn_frame.pack()
            self.manifest_operation_run_btn.pack(pady=10, side="left")
            self.manifest_operation_sublime_btn.pack(side="right")
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.manifest_operation_run_btn.configure(state="normal")
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "DECOMPILE APK":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_frame.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack()
            self.decompile_option_lable.pack(side="left", padx=10)
            self.decompile_option_dropdown.pack(side="right", padx=10, pady=10)
            self.compile_decompile_run_btn_frame.pack()
            self.compile_decompile_sublime_btn.pack(side="right")
            self.compile_decompile_run_btn.pack(pady=10, side="left")
            self.compile_decompile_run_btn.configure(state="normal",text="DECOMPILE APK", width=310)
            self.decompile_output_textbox.pack(pady=10)
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "COMPILE PROJECT":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.compile_decompile_run_btn_frame.pack()
            self.compile_decompile_run_btn.pack(pady=10)
            self.compile_decompile_run_btn.pack(pady=10)
            self.compile_decompile_run_btn.configure(state="normal",text="COMPILE APK PROJECT", width=360)
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack(side="left", padx=10)
            self.compile_option_dropdown.pack(side="right", padx=10, pady=10)
            self.compile_output_textbox.pack(pady=10)
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "CRC32 RESTORE":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack()
            self.crc32_option_lable.pack()
            self.crc32_frame_sub.pack()
            self.crc32_original_apk_entry.pack(side="left", padx =10)
            self.crc32_original_apk_pick_btn.pack(side="right", padx=10)
            self.crc32_run_btn.pack(pady=10)
            self.crc32_output_textbox.pack()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "REPLACE APK CONTENT":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.antisplit_frame.pack_forget()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack()
            self.replace_frame_sub.pack()
            self.replace_content_entry.pack(side="left", padx=10, pady=5)
            self.replace_content_pick_btn.pack(side="right", padx=10, pady=5)
            self.replace_run_btn.pack(pady=10)
            self.replace_output_textbox.pack(pady=3)
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "DEX2SMALI":
            self.signature_verify_frame.pack_forget()
            self.antisplit_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack()
            self.dex2smali_option_lable.pack(side="left", padx=10)
            self.dex2smali_option_dropdown.pack(side="right", padx=10, pady=5)
            self.dex2smali_frame_sub.pack()
            self.dex2smali_manual_option_lable.pack(side="left", padx=10)
            self.dex2smali_dex_name_entry.pack(side="right", padx=10, pady=5)
            self.dex2smali_run_btn.pack(pady=5)
            self.dex2smali_output_textbox.pack(pady=10)
            self.dex2smali_run_btn.configure(state="normal")
            self.get_dex_file_list()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "SMALI2DEX":
            self.signature_verify_frame.pack_forget()
            self.antisplit_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.get_smali_folder_list()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack()
            self.smali2dex_frame_sub.pack()
            self.smali2dex_option_lable.pack(side="left", padx=10)
            self.smali2dex_option_dropdown.pack(side="right", padx=10, pady=5)
            self.smali2dex_manual_option_lable.pack(side="left", padx=10)
            self.smali2dex_smali_name_entry.pack(side="right", padx=10, pady=5)
            self.smali2dex_run_btn.pack(pady=5)
            self.smali2dex_output_textbox.pack(pady=10)
            self.smali2dex_run_btn.configure(state="normal")
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack_forget()
            self.arsc_tool_option_lable.pack_forget()
            self.arsc_tool_option_dropdown.pack_forget()
            self.arsc_tool_run_btn_frame.pack_forget()
            self.arsc_tool_run_btn.pack_forget()
            self.arsc_tool_sublime_btn.pack_forget()
            self.arsc_tool_output_textbox.pack_forget()
            self.arsc_tool_editor_btn.pack_forget()

       elif self.apk_function_dropdown.get() == "ARSC OPERATIONS":
            self.signature_verify_frame.pack_forget()
            self.other_function_frame.pack()
            self.run_button_other.pack_forget()
            self.antisplit_frame.pack_forget()
            self.antisplit_output_textbox.pack_forget()
            self.protect_output_textbox.pack_forget()
            self.sign_output_textbox.pack_forget()
            self.refact_output_textbox.pack_forget()
            self.signaturekill_output_textbox.pack_forget()
            self.manifest_operation_output_textbox.pack_forget()
            self.signaturekill_option_dropdown.pack_forget()
            self.protect_run_btn.pack_forget()
            self.protect_option_lable.pack_forget()
            self.protect_option_dropdown.pack_forget()
            self.protect_frame.pack_forget()
            self.compile_decompile_frame.pack_forget()
            self.decompile_option_lable.pack_forget()
            self.decompile_option_dropdown.pack_forget()
            self.compile_decompile_run_btn_frame.pack_forget()
            self.compile_decompile_sublime_btn.pack_forget()
            self.compile_decompile_run_btn.pack_forget()
            self.compile_decompile_run_btn.configure()
            self.decompile_output_textbox.pack_forget()
            self.compile_option_lable.pack_forget()
            self.compile_option_dropdown.pack_forget()
            self.compile_output_textbox.pack_forget()
            self.signaturekill_run_btn.pack_forget()
            self.signaturekill_frame.pack_forget()
            self.signaturekill_option_lable.pack_forget()
            self.manifest_operation_frame.pack_forget()
            self.manifest_operation_run_btn.pack_forget()
            self.manifest_operation_option_dropdown.pack_forget()
            self.manifest_operation_option_lable.pack_forget()
            self.sign_frame.pack_forget()
            self.sign_option_lable.pack_forget()
            self.sign_option_dropdown.pack_forget()
            self.sign_run_btn.pack_forget()
            self.crc32_frame.pack_forget()
            self.crc32_option_lable.pack_forget()
            self.crc32_frame_sub.pack_forget()
            self.crc32_original_apk_entry.pack_forget()
            self.crc32_original_apk_pick_btn.pack_forget()
            self.crc32_run_btn.pack_forget()
            self.crc32_output_textbox.pack_forget()
            self.replace_frame.pack_forget()
            self.replace_frame_sub.pack_forget()
            self.replace_content_entry.pack_forget()
            self.replace_content_pick_btn.pack_forget()
            self.replace_run_btn.pack_forget()
            self.replace_output_textbox.pack_forget()
            self.antisplit_option_lable.pack_forget()
            self.antisplit_option_dropdown.pack_forget()
            self.dex2smali_frame.pack_forget()
            self.dex2smali_option_lable.pack_forget()
            self.dex2smali_option_dropdown.pack_forget()
            self.dex2smali_run_btn.pack_forget()
            self.dex2smali_output_textbox.pack_forget()
            self.dex2smali_frame_sub.pack_forget()
            self.dex2smali_manual_option_lable.pack_forget()
            self.dex2smali_dex_name_entry.pack_forget()
            self.run_button_default.pack_forget()
            self.output_default_textbox.pack_forget()
            self.smali2dex_frame.pack_forget()
            self.smali2dex_frame_sub.pack_forget()
            self.smali2dex_option_lable.pack_forget()
            self.smali2dex_option_dropdown.pack_forget()
            self.smali2dex_manual_option_lable.pack_forget()
            self.smali2dex_smali_name_entry.pack_forget()
            self.smali2dex_run_btn.pack_forget()
            self.smali2dex_output_textbox.pack_forget()
            self.manifest_operation_run_btn_frame.pack_forget()
            self.manifest_operation_sublime_btn.pack_forget()
            self.arsc_tool_frame.pack()
            self.arsc_tool_option_lable.pack(side="left", padx=10)
            self.arsc_tool_option_dropdown.pack(side="right", padx=10, pady=10)
            self.arsc_tool_run_btn_frame.pack()
            self.arsc_tool_run_btn.configure(state="normal",text="DUMP/COMPILE ARSC", width=260)
            self.arsc_tool_run_btn.pack(pady=10, side="left")
            self.arsc_tool_editor_btn.pack(side="right")
            self.arsc_tool_sublime_btn.pack(side="right")
            self.arsc_tool_output_textbox.pack()

       self.apk_function_confirm_btn.configure(state="disabled", fg_color=BTN_COLOR)
       self.apk_picker_btn.configure(state="disabled")
       self.apk_function_dropdown.configure(state="disabled")
       self.apk_function_reset_btn.configure(state="normal", fg_color="#FF0000")



    def browse_apk(self):
            filename = filedialog.askopenfilename(title="Select APK File", filetypes=(("APK files", "*.apk;*.apks;*.apkm;*.zip;*.xapk"), ("All files", "*.*")))

            self.apk_detail_output_textbox.configure(state="normal")
            self.apk_detail_output_textbox.delete(1.0, "end")
            self.apk_detail_output_textbox.insert("end", "")
            self.apk_detail_output_textbox.configure(state="disabled")
            self.apk_logo_lable.configure(image=default_icon)

            if filename:
                self.apk_entry.delete(0, "end")
                self.apk_entry.insert(0, filename)
                self.apk_info_button.configure(state="normal")



    def browse_original_apk(self):
            filename = filedialog.askopenfilename(title="Select APK File", filetypes=(("APK files", "*.apk"), ("All files", "*.*")))

            if filename:
                self.crc32_original_apk_entry.delete(0, "end")
                self.crc32_original_apk_entry.insert(0, filename)
                self.crc32_run_btn.configure(state="normal")



    def browse_replacement_file(self):
            filename = filedialog.askopenfilenames(title="Select A File", filetypes=(("All files", "*.dex;*.xml;*.arsc"), ("All files", "*.*")))

            if filename:
                self.replace_content_entry.delete(0, "end")
                self.replace_content_entry.insert(0, filename)
                self.replace_run_btn.configure(state="normal")



    def extract_application_info(self):

        self.apk_function_confirm_btn.configure(state="normal", fg_color="#0E8849")
        self.apk_detail_copy_btn.configure(state="normal")
        self.apk_explore_btn.configure(state="normal")
        apk_path = self.apk_entry.get()
        size_in_bytes = os.path.getsize(apk_path)
        size_in_mb = size_in_bytes / (1024 * 1024)

        if self.apk_entry.get().endswith('.apkm') or self.apk_entry.get().endswith('.apks') or self.apk_entry.get().endswith('.zip') or self.apk_entry.get().endswith('.xapk'):
            self.apk_function_dropdown.configure(values=functions_apks)
            self.apk_function_dropdown.set("MERGE BUNDLE")

            try:
                with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                    zip_ref.extractall('Temporary\\bin')
                    base_apk_path = os.path.join('Temporary', 'bin', 'base.apk')
                    with zipfile.ZipFile(base_apk_path, 'r') as zip_ref_:

                        script_dir = os.path.dirname(os.path.abspath(__file__))

                        apkeditor_jar_filepath = "java_Packages\\APKEditor.jar"
                        apkeditor_jar_filepath_ = os.path.join(script_dir, apkeditor_jar_filepath)

                        java_command = f"java -jar {apkeditor_jar_filepath_} info -v -app-name -app-icon -version-name -min-sdk-version -target-sdk-version -package -app-class -i {base_apk_path}"
                        output = subprocess.check_output(java_command, shell=True, text=True)
                    
                        try:
                            for line in output.split('\n'):
                                if '(-xxhdpi)' in line:
                                    app_icon_dir = line.split()[-1]
                                    try:
                                        with zip_ref_.open(app_icon_dir) as icon_file:
                                            app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                            self.apk_logo_lable.configure(image=app_icon)
                                    except:
                                            try:
                                                app_icon_file = os.path.join('Temporary', 'bin', 'icon.png')
                                                app_icon = CTkImage(Image.open(app_icon_file), size=(60, 60))
                                                self.apk_logo_lable.configure(image=app_icon)
                                            except:
                                                self.apk_logo_lable.configure(image=default_icon)

                                elif '(-xhdpi)' in line:
                                    app_icon_dir = line.split()[-1]

                                    try:
                                        with zip_ref_.open(app_icon_dir) as icon_file:
                                            app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                            self.apk_logo_lable.configure(image=app_icon)
                                    except:
                                            try:
                                                app_icon_file = os.path.join('Temporary', 'bin', 'icon.png')
                                                app_icon = CTkImage(Image.open(app_icon_file), size=(60, 60))
                                                self.apk_logo_lable.configure(image=app_icon)
                                            except:
                                                self.apk_logo_lable.configure(image=default_icon)

                                elif '(-xxxhdpi)' in line:
                                    app_icon_dir = line.split()[-1]
                                    try:
                                        with zip_ref_.open(app_icon_dir) as icon_file:
                                            app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                            self.apk_logo_lable.configure(image=app_icon)
                                    except:
                                            try:
                                                app_icon_file = os.path.join('Temporary', 'bin', 'icon.png')
                                                app_icon = CTkImage(Image.open(app_icon_file), size=(60, 60))
                                                self.apk_logo_lable.configure(image=app_icon)
                                            except:
                                                self.apk_logo_lable.configure(image=default_icon)

                                elif '.xml' in line:
                                    self.apk_logo_lable.configure(image=default_icon)

                        except:
                            try:
                                app_icon_file = os.path.join('Temporary', 'bin', 'icon.png')
                                app_icon = CTkImage(Image.open(app_icon_file), size=(60, 60))
                                self.apk_logo_lable.configure(image=app_icon)
                            except:
                                self.apk_logo_lable.configure(image=default_icon)
                        
                        for line in output.split('\n'):
                            if '()' in line and '/' not in line:
                                app_name = line[14:]

                        for line in output.split('\n'):
                            if 'VersionName=' in line:
                                version_name = line.split('"')[1]

                        for line in output.split('\n'):
                            if 'application-class=' in line:
                                application_name = line.split('"')[1]
                                if application_name == "com.pairip.application.Application":
                                    protector = "Google加固"
                                elif application_name == "MyWrapperProxyApplication":
                                    protector = "腾讯皇家安防 (Tencent Royal)"
                                elif application_name == "com.stub.StubApp":
                                    protector = "360加固 Jiagu"
                                else:
                                    protector = "No Protection"

                        for line in output.split('\n'):
                            if 'package=' in line:
                                package_phrase = line.split('"')[1]

                        for line in output.split('\n'):
                            if 'MinSdkVersion=' in line:
                                minsdk = line.split('"')[1]

                        for line in output.split('\n'):
                            if 'TargetSdkVersion=' in line:
                                targetsdk = line.split('"')[1]
                        
                        num_of_splits = self.count_apks_in_bundle(apk_path)

                        global packID
                        packID = package_phrase

                        self.apk_detail_output_textbox.configure(state="normal")
                        self.apk_detail_output_textbox.delete(1.0, "end")
                        self.apk_detail_output_textbox.insert("end", f"APK-Bundle Information: {app_name}\n----------------------\n1.Package: {package_phrase}\n2.Application Name: {application_name}\n3.Version: {version_name}\n4.Min-SDK: {minsdk}\n5.Target-SDK: {targetsdk}\n6.Split APK: {num_of_splits}\n7.Protection: {protector}\n8.File Size: {size_in_mb:.2f} MB")
                        self.apk_detail_output_textbox.configure(state="disabled")

            except FileNotFoundError:
                print("APK file not found.")

            except Exception as e:
                self.apk_detail_output_textbox.configure(state="normal")
                self.apk_detail_output_textbox.delete(1.0, "end")
                self.apk_detail_output_textbox.insert("end", f"APK-Bundle Information: {app_name}\n----------------------\n1.Package: {package_phrase}\n2.Application Name: {application_name}\n3.Version: {version_name}\n4.Min-SDK: {minsdk}\n5.Target-SDK: {targetsdk}\n6.Last DEX File: {last_dex_file}\n7.Protection: {protector}\n8.File Size: {size_in_mb:.2f} MB")
                self.apk_detail_output_textbox.configure(state="disabled")

        else:
            apk_path = self.apk_entry.get()
            self.apk_function_dropdown.configure(values=functions_apk)
            self.apk_function_dropdown.set("VERIFY SIGNATURE")

            size_in_bytes = os.path.getsize(apk_path)
            size_in_mb = size_in_bytes / (1024 * 1024)

            try:
                with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                    file_list = zip_ref.namelist()

                    if any(fname.startswith('lib/') for fname in file_list):
                        lib_folder_contents = [fname for fname in file_list if fname.startswith('lib/')]
                        lib_subfolders = []

                        for item in lib_folder_contents:
                            if item.startswith('lib/') and '/' in item[len('lib/'):]:
                                subfolder = item[len('lib/'):].split('/')[0]
                                if subfolder not in lib_subfolders:
                                    lib_subfolders.append(subfolder)
                        if lib_subfolders:
                            arch = ", ".join(lib_subfolders)
                        else:
                            arch = "No Architecture"
                    else:
                        arch = "No Architecture"
                 
                    script_dir = os.path.dirname(os.path.abspath(__file__))

                    apkeditor_jar_filepath = "java_Packages\\APKEditor.jar"
                    apkeditor_jar_filepath_ = os.path.join(script_dir, apkeditor_jar_filepath)

                    java_command = f"java -jar {apkeditor_jar_filepath_} info -v -app-icon -app-name -version-name -min-sdk-version -target-sdk-version -dex -package -app-class -i {apk_path}"
                    output = subprocess.check_output(java_command, shell=True, text=True)

                    try:
                        for line in output.split('\n'):
                            if '(-xxhdpi)' in line:
                                app_icon_directory = line.split()[-1]
                                with zip_ref.open(app_icon_directory) as icon_file:
                                    app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                    self.apk_logo_lable.configure(image=app_icon)

                            elif '(-xxxhdpi)' in line:
                                app_icon_directory = line.split()[-1]
                                with zip_ref.open(app_icon_directory) as icon_file:
                                    app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                    self.apk_logo_lable.configure(image=app_icon)

                            elif '(-xhdpi)' in line:
                                app_icon_directory = line.split()[-1]
                                with zip_ref.open(app_icon_directory) as icon_file:
                                    app_icon = CTkImage(Image.open(icon_file), size=(60, 60))
                                    self.apk_logo_lable.configure(image=app_icon)

                            elif '.xml' in line:
                                self.apk_logo_lable.configure(image=default_icon)
                    except:
                        print("Unable to extract Icon")
                    
                    for line in output.split('\n'):
                        if '()' in line and '/' not in line:
                            app_name = line[14:]

                    for line in output.split('\n'):
                        if 'VersionName=' in line:
                            version_name = line.split('"')[1]

                    for line in output.split('\n'):
                        if 'application-class=' in line:
                            application_name = line.split('"')[1]
                            if application_name == "com.pairip.application.Application":
                                protector = "Google加固"
                            elif application_name == "MyWrapperProxyApplication":
                                protector = "腾讯皇家安防 (Tencent Royal)"
                            elif application_name == "com.stub.StubApp":
                                protector = "360加固 Jiagu"
                            else:
                                protector = "No Protection"

                    for line in output.split('\n'):
                        if 'package=' in line:
                            package_phrase = line.split('"')[1]

                    for line in output.split('\n'):
                        if 'MinSdkVersion=' in line:
                            minsdk = line.split('"')[1]

                    for line in output.split('\n'):
                        if 'TargetSdkVersion=' in line:
                            targetsdk = line.split('"')[1]

                    dex_file_names = re.findall(r'Name="([^"]+)"', output)
                    if dex_file_names:
                        last_dex_file = dex_file_names[-1]
                    else:
                        last_dex_file = ""

                    global packID_
                    packID_ = package_phrase
                 
                    self.apk_detail_output_textbox.configure(state="normal")
                    self.apk_detail_output_textbox.delete(1.0, "end")
                    self.apk_detail_output_textbox.insert("end", f"APK Information: {app_name}\n----------------\n1.Package: {package_phrase}\n2.Application Name: {application_name}\n3.Version: {version_name}\n4.Min-SDK: {minsdk}\n5.Target-SDK: {targetsdk}\n6.Last DEX File: {last_dex_file}\n7.Architecture: {arch}\n8.Protection: {protector}\n9.File Size: {size_in_mb:.2f} MB")
                    self.apk_detail_output_textbox.configure(state="disabled")

            except FileNotFoundError:
                print("APK file not found.")
                
            except Exception as e:
                self.apk_detail_output_textbox.configure(state="normal")
                self.apk_detail_output_textbox.delete(1.0, "end")
                self.apk_detail_output_textbox.insert("end", f"APK Information: {app_name}\n----------------\n1.Package: {package_phrase}\n2.Application Name: {application_name}\n3.Version: {version_name}\n4.Min-SDK: {minsdk}\n5.Target-SDK: {targetsdk}\n6.Last DEX File: {last_dex_file}\n7.Architecture: {arch}\n8.Protection: {protector}\n9.File Size: {size_in_mb:.2f} MB")
                self.apk_detail_output_textbox.configure(state="disabled")

                if not apk_path:
                    self.apk_entry.configure(placeholder_text="Please Select APK")
                    return



    def execution_on_thread(self):
        threading.Thread(target=self.function_execution).start()



    def function_execution(self):
        self.apk_function_reset_btn.configure(state="disabled", fg_color=BTN_COLOR)
        self.apk_picker_btn.configure(state="normal")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        sigtool_jar_filepath = "java_Packages\\SigTools.jar"
        sigtool_jar_filepath_ = os.path.join(script_dir, sigtool_jar_filepath)

        apkeditor_jar_filepath = "java_Packages\\APKEditor.jar"
        apkeditor_jar_filepath_ = os.path.join(script_dir, apkeditor_jar_filepath)

        signer_jar_filepath = "java_Packages\\APKSigner.jar"
        signer_jar_filepath_ = os.path.join(script_dir, signer_jar_filepath)

        jks_filepath = "Keystore\\AppStaticsX™.keystore"
        jks_filepath_ = os.path.join(script_dir, jks_filepath)

        dex_guard_jar_filepath = "java_Packages\\DexGuard.jar"
        dex_guard_jar_filepath_ = os.path.join(script_dir, dex_guard_jar_filepath)

        apktool_jar_filepath = "java_Packages\\APKTool.jar"
        apktool_jar_filepath_ = os.path.join(script_dir, apktool_jar_filepath)

        baksmali_jar_filepath = "Java_Packages\\baksmali-2.5.2.jar"
        baksmali_jar_filepath_ = os.path.join(script_dir, baksmali_jar_filepath)

        smali_jar_filepath = "Java_Packages\\smali-2.5.2.jar"
        smali_jar_filepath_ = os.path.join(script_dir, smali_jar_filepath)

        arsc_jar_filepath = "Java_Packages\\arsctool.jar"
        arsc_jar_filepath_ = os.path.join(script_dir, arsc_jar_filepath)

        crc32_jar_filepath = "Java_Packages\\CRC32Restorer.jar"
        crc32_jar_filepath_ = os.path.join(script_dir, crc32_jar_filepath)

        out_dir = os.path.dirname(self.apk_entry.get())

        selected_format = self.signature_verify_format_option_dropdown.get()
        output_format = self.signature_verify_output_format_option_dropdown.get()

        apk_filename = self.apk_entry.get()
        apk_file = os.path.join(script_dir, apk_filename)

        out_dir_abs = os.path.splitext(apk_filename)[0]

        selected_format = self.signature_verify_format_option_dropdown.get()
        output_format = self.signature_verify_output_format_option_dropdown.get()

        original_apk = self.crc32_original_apk_entry.get()
        original_apk_path = os.path.join(script_dir, original_apk)

        application_name = os.path.basename(apk_filename)

        smali_dir = self.smali2dex_smali_name_entry.get()

        dex_file = self.dex2smali_dex_name_entry.get()


# Verify_APK_Signature
        if self.apk_function_dropdown.get() == "VERIFY SIGNATURE":

            self.run_button_default.configure(fg_color="#0E8849")
            self.output_default_textbox.insert("end", f"Verifying APK ...\n\nInput: {apk_filename}")
            java_command = f"java -jar {sigtool_jar_filepath_} GetCert -INFORM APK -OUTFORM {selected_format} -IN {apk_file} -OUTFILE {apk_file}{output_format}"  

            process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return_code = process.returncode

            self.output_default_textbox.configure(state="normal")
            self.run_button_default.configure(fg_color=BTN_COLOR)
            self.output_default_textbox.insert("end", f"\nVerifying Certificate ({selected_format})...\nOutput:\n{apk_file}{output_format} (Sucessfully Verified)\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}")
            self.output_default_textbox.configure(state="disabled")


# CRC32_Restore_Function         
        elif self.apk_function_dropdown.get() == "CRC32 RESTORE":

            self.crc32_run_btn.configure(fg_color="#0E8849")
            self.crc32_output_textbox.insert("end", f"Patching APK ...\nOriginal APK: {original_apk_path}\nModified APK: {apk_file}\n")
            java_command = f"java -jar {crc32_jar_filepath_} {original_apk_path} {apk_file}"  

            process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return_code = process.returncode

            self.crc32_output_textbox.configure(state="normal")
            self.crc32_run_btn.configure(fg_color=BTN_COLOR)
            self.crc32_output_textbox.insert("end", f"\nOutput:\n{out_dir_abs}+_crc_restored.apk\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}")
            self.crc32_output_textbox.configure(state="disabled")


# Replace_APK_content
        elif self.apk_function_dropdown.get() == "REPLACE APK CONTENT":
            self.replace_run_btn.configure(fg_color="#0E8849")
            self.replace_output_textbox.configure(state="normal")
            self.replace_output_textbox.insert("end", f"Replacing APK File ...\nInput APK: {apk_filename}\n")
            self.replace_output_textbox.insert("end", "Please Wait ...\n")
            self.replace_file_in_apk()
            self.replace_run_btn.configure(fg_color=BTN_COLOR)


# AntiSplit_Function
        elif self.apk_function_dropdown.get() == "MERGE BUNDLE":

            self.run_button_other.configure(fg_color="#0E8849")

            if self.antisplit_option_dropdown.get() == "OBFUSCATE":
                self.antisplit_output_textbox.delete(1.0, "end")
                self.antisplit_output_textbox.insert("end", f"Merging APK-Bundle ...:\n{"[MERGE] Merging..."}\n{"Input File: "+apk_file}\n")
                java_command = f"java -jar {apkeditor_jar_filepath_} m -i {apk_file} -res-dir kotlin/meta-data/global"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.antisplit_output_textbox.configure(state="normal")
                self.run_button_other.configure(fg_color=BTN_COLOR)
                self.antisplit_output_textbox.insert("end", f"\n{"Output File: "+apk_file+"_merged.apk"}\n{"I: [MERGE] Extracting ...\nI: [MERGE] Searching apk files ...\nI: [MERGE] Finding apk files ...\n\nI: [MERGE] Merging string pools ... \nI: [MERGE] Merging: base\nI: [MERGE] Added [base] classes.dex -> classes.dex\nI: [MERGE] Merging resource table: base\nI: [MERGE] Merging resource table: split_apk(s)\n\nI: [MERGE] Sanitizing manifest ...\nI: [MERGE] Removed-attribute : requiredSplitTypes\nI: [MERGE] Removed-attribute : splitTypes\nI: [MERGE] Removed-attribute : extractNativeLibs\nI: [MERGE] Removed-attribute : isSplitRequired\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.splits.required\nI: [MERGE] Removed-element : <meta-data> name=com.android.stamp.source\nI: [MERGE] Removed-element : <meta-data> name=com.android.stamp.type\nI: [MERGE] Removed-table-entry : res/xml/splits0.xml\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.splits\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.derived.apk.id\nI: [MERGE] Removed unused table strings = 1\n\nTable size changed\nI: [MERGE] Writing apk ...\nI: [MERGE] Buffering compress changed files ...\nI: [MERGE] Writing files ...\nI: [MERGE] Obfuscating Resources ...\n\nI: [MERGE] Saved to:"+apk_file+"_merged.apk"}\nError:\nReturn Code: {return_code}\n\n")
                self.antisplit_output_textbox.configure(state="disabled")
            else:
                self.antisplit_output_textbox.delete(1.0, "end")
                self.antisplit_output_textbox.insert("end", f"Merging APK-Bundle ...:\n{"[MERGE] Merging..."}\n{"Input File: "+apk_file}\n")
                java_command = f"java -jar {apkeditor_jar_filepath_} m -i {apk_file}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.antisplit_output_textbox.configure(state="normal")
                self.run_button_other.configure(fg_color=BTN_COLOR)
                self.antisplit_output_textbox.insert("end", f"{"Output File"+apk_file+"_merged.apk"}\n{"I: [MERGE] Extracting ...\nI: [MERGE] Searching apk files ...\nI: [MERGE] Finding apk files ...\n\nI: [MERGE] Merging string pools ... \nI: [MERGE] Merging: base\nI: [MERGE] Added [base] classes.dex -> classes.dex\nI: [MERGE] Merging resource table: base\nI: [MERGE] Merging resource table: split_apk(s)\n\nI: [MERGE] Sanitizing manifest ...\nI: [MERGE] Removed-attribute : requiredSplitTypes\nI: [MERGE] Removed-attribute : splitTypes\nI: [MERGE] Removed-attribute : extractNativeLibs\nI: [MERGE] Removed-attribute : isSplitRequired\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.splits.required\nI: [MERGE] Removed-element : <meta-data> name=com.android.stamp.source\nI: [MERGE] Removed-element : <meta-data> name=com.android.stamp.type\nI: [MERGE] Removed-table-entry : res/xml/splits0.xml\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.splits\nI: [MERGE] Removed-element : <meta-data> name=com.android.vending.derived.apk.id\nI: [MERGE] Removed unused table strings = 1\n\nTable size changed\nI: [MERGE] Writing apk ...\nI: [MERGE] Buffering compress changed files ...\nI: [MERGE] Writing files ...\n\nI: [MERGE] Saved to:"+apk_file+"_merged.apk"}\nError:\nReturn Code: {return_code}\n\n")
                self.antisplit_output_textbox.configure(state="disabled")

            self.delete_temp()


# Sign_APK_Function
        elif self.apk_function_dropdown.get() == "SIGN APK":

            self.sign_run_btn.configure(fg_color="#0E8849")
            self.sign_output_textbox.insert("end", f"Signing APK ...\n{apk_file}")

            if self.sign_option_dropdown.get() == "ZIPALIGN":
                java_command = f"java -jar {signer_jar_filepath_} -a {apk_file} -o {out_dir} --ks {jks_filepath_} --ksAlias AppStaticsX --ksPass AppStaticsX@ASUS --ksKeyPass AppStaticsX@ASUS --allowResign"  

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.sign_output_textbox.configure(state="normal")
                self.sign_run_btn.configure(fg_color=BTN_COLOR)
                self.sign_output_textbox.insert("end", f"\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.sign_output_textbox.configure(state="disabled")

            else:
                java_command = f"java -jar {signer_jar_filepath_} -a {apk_file} -o {out_dir} --ks {jks_filepath_} --ksAlias AppStaticsX --ksPass AppStaticsX@ASUS --ksKeyPass AppStaticsX@ASUS -skipZipAlign --allowResign"  

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.sign_output_textbox.configure(state="normal")
                self.sign_run_btn.configure(fg_color=BTN_COLOR)
                self.sign_output_textbox.insert("end", f"\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.sign_output_textbox.configure(state="disabled")


# DEX_to_Smali_Function
        elif self.apk_function_dropdown.get() == "DEX2SMALI":

            self.dex2smali_run_btn.configure(fg_color="#0E8849")
            self.dex2smali_output_textbox.insert("end", f"Decompiling DEX File ...\nApplication: {application_name}\nbaksmali-2.5.2 Working On ...")

            if self.dex2smali_option_dropdown.get() == "MANUAL":
                output_ = os.path.dirname(self.apk_entry.get())
                file_name = os.path.basename(apk_filename)
                output_dir = output_+"\\"+"DexDump_"+os.path.splitext(file_name)[0]

                dex_file_path = os.path.join(output_dir, dex_file)

                output_dir_classes = os.path.join(output_dir, "DexDump", "smali_"+dex_file[:-4])

                java_command = f"java -jar {baksmali_jar_filepath_} d {dex_file_path} -o {output_dir_classes}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.dex2smali_output_textbox.configure(state="normal")
                self.dex2smali_run_btn.configure(fg_color=BTN_COLOR)
                self.dex2smali_output_textbox.insert("end", f"\n\nDecompiling DEX: {dex_file}\nDecompile Sucessfull ...\nOutput: {output_dir_classes}")
                self.dex2smali_output_textbox.configure(state="disabled")


# Smali_to_DEX_Function
        elif self.apk_function_dropdown.get() == "SMALI2DEX":
                
                self.smali2dex_run_btn.configure(fg_color="#0E8849")
                self.smali2dex_output_textbox.insert("end", f"Compiling to DEX File ...\nsmali-2.5.2 Working On ...")

                if self.smali2dex_option_dropdown.get() == "MANUAL":
          
                    input_ = os.path.dirname(self.apk_entry.get())
                    file_name = os.path.basename(apk_filename)
                    input_dir = input_+"\\"+"DexDump_"+os.path.splitext(file_name)[0]+"\\"+"DexDump"

                    smali_file_path = os.path.join(input_dir, smali_dir)

                    output_dir_dexes = os.path.join(input_dir, smali_dir[6:]+".dex")

                    java_command = f"java -jar {smali_jar_filepath_} assemble {smali_file_path} -o {output_dir_dexes}"

                    process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    return_code = process.returncode

                    self.smali2dex_output_textbox.configure(state="normal")
                    self.smali2dex_run_btn.configure(fg_color=BTN_COLOR)
                    self.smali2dex_output_textbox.insert("end", f"\n\nCompiling Folder: {smali_file_path}\nCompile Sucessfull ...\nOutput: {output_dir_dexes}")
                    self.smali2dex_output_textbox.configure(state="disabled")


# Decompile_Function
        elif self.apk_function_dropdown.get() == "DECOMPILE APK":

            self.compile_decompile_run_btn.configure(fg_color="#0E8849")
            self.decompile_output_textbox.insert("end", f"Decompiling APK ...\n{apk_file}\nAPKTool v2.9.3 Working on ...\n")

            if self.decompile_option_dropdown.get() == "DEX FILES":
                java_command = f"java -jar {apktool_jar_filepath_} d -r -only-main-classes -o {out_dir_abs} {apk_file}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.decompile_output_textbox.configure(state="normal")
                self.compile_decompile_run_btn.configure(fg_color=BTN_COLOR)
                self.decompile_output_textbox.insert("end", f"\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.decompile_output_textbox.configure(state="disabled")

            else:
                java_command = f"java -jar {apktool_jar_filepath_} d -s -o {out_dir_abs} {apk_file}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.decompile_output_textbox.configure(state="normal")
                self.compile_decompile_run_btn.configure(fg_color=BTN_COLOR)
                self.decompile_output_textbox.insert("end", f"\n\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.decompile_output_textbox.configure(state="disabled")

            self.compile_decompile_sublime_btn.configure(state="normal", image=sublime_icon_enable)


# ARSC_Function
        elif self.apk_function_dropdown.get() == "ARSC OPERATIONS":

            self.arsc_tool_run_btn.configure(fg_color="#0E8849")
            output_ = os.path.dirname(apk_filename)
            file_name = os.path.basename(apk_filename)
            output_dir = output_+"\\"+"ARSC_"+os.path.splitext(file_name)[0]
            target_file = output_dir+"\\"+"resources.arsc"
            dump_dir = output_dir+"\\"+"res.xml"

            if self.arsc_tool_option_dropdown.get() == "DUMP":
                self.arsc_tool_output_textbox.insert("end", f"Decompiling resources.arsc ...\nInput File{apk_filename}\nARSCTool v0.0.2 Working on ...\n")
                os.makedirs(output_dir, exist_ok=True)

                with zipfile.ZipFile(apk_filename, 'r') as apk_zip:
                    apk_file_list = apk_zip.namelist()
                    for file in apk_file_list:
                        if file.endswith('.arsc'):
                            apk_zip.extract(file, output_dir)

                java_command = f"java -jar {arsc_jar_filepath_} d -i {target_file} -o {dump_dir}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.arsc_tool_output_textbox.configure(state="normal")
                self.arsc_tool_run_btn.configure(fg_color=BTN_COLOR)
                self.arsc_tool_output_textbox.insert("end", f"\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.arsc_tool_output_textbox.configure(state="disabled")

            else:
                compiled_save_dir = output_dir+"\\"+"re_resources.arsc"
                self.arsc_tool_output_textbox.delete(1.0, "end")
                self.arsc_tool_output_textbox.insert("end", f"Compiling resources.arsc ...\nInput File{apk_filename}\nARSCTool v0.0.2 Working on ...\n")
                java_command = f"java -jar {arsc_jar_filepath_} b -i {dump_dir} -o {compiled_save_dir}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.arsc_tool_output_textbox.configure(state="normal")
                self.arsc_tool_run_btn.configure(fg_color=BTN_COLOR)
                self.arsc_tool_output_textbox.insert("end", f"\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.arsc_tool_output_textbox.configure(state="disabled")

            self.arsc_tool_sublime_btn.configure(state="normal", image=sublime_icon_enable)
            self.arsc_tool_editor_btn.configure(state="normal")


# Compile_Function
        elif self.apk_function_dropdown.get() == "COMPILE PROJECT":
            self.compile_decompile_run_btn.configure(fg_color="#0E8849")
            self.compile_output_textbox.insert("end", f"Compiling APK Project ...\n{out_dir_abs}\nAPKTool v2.9.3 Working on ...\n")

            if self.compile_option_dropdown.get() == "AAPT2":
                java_command = f"java -jar {apktool_jar_filepath_} b -use-aapt2 {out_dir_abs}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.compile_output_textbox.configure(state="normal")
                self.compile_decompile_run_btn.configure(fg_color=BTN_COLOR)
                self.compile_output_textbox.insert("end", f"\nCompiling APK Project ...\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.compile_output_textbox.configure(state="disabled")

            else:
                java_command = f"java -jar {apktool_jar_filepath_} b -use-aapt {out_dir_abs}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.compile_output_textbox.configure(state="normal")
                self.compile_decompile_run_btn.configure(fg_color=BTN_COLOR)
                self.compile_output_textbox.insert("end", f"\nCompiling APK Project ...\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.compile_output_textbox.configure(state="disabled")


# Refact_Resources_Function
        elif self.apk_function_dropdown.get() == "REFACT RESOURCE":

            self.run_button_other.configure(fg_color="#0E8849")
            self.refact_output_textbox.insert("end", f"Refacting APK Resources ...\nInput: {apk_file}\nAPKEditor v6.8.1 Working on ...\n")
            java_command = f"java -jar {apkeditor_jar_filepath_} x -i {apk_file}" 

            process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return_code = process.returncode

            self.refact_output_textbox.configure(state="normal")
            self.run_button_other.configure(fg_color=BTN_COLOR)
            self.refact_output_textbox.insert("end", f"\n{stderr.decode()}")
            self.refact_output_textbox.configure(state="disabled")


# APK_Protect_Function
        elif self.apk_function_dropdown.get() == "PROTECT APK":

            self.protect_run_btn.configure(fg_color="#0E8849")
            self.protect_output_textbox.insert("end", f"Protecting APK Resources ...\nInput: {apk_file}\nDexGuard Working on ...")

            if self.protect_option_dropdown.get() == "DEX":
                java_command = f"java -jar {dex_guard_jar_filepath_} -o {out_dir} {apk_file}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.protect_output_textbox.configure(state="normal")
                self.protect_run_btn.configure(fg_color=BTN_COLOR)
                self.protect_output_textbox.insert("end", f"\n\nProtecting APK DEX Files ...\n{stdout.decode()}\nError:\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.protect_output_textbox.configure(state="disabled")

            else:
                java_command = f"java -jar {apkeditor_jar_filepath_} p -i {apk_file}"

                process = subprocess.Popen(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                return_code = process.returncode

                self.protect_output_textbox.configure(state="normal")
                self.protect_run_btn.configure(fg_color=BTN_COLOR)
                self.protect_output_textbox.insert("end", f"\n\nProtecting APK Resources ...\n{stderr.decode()}\nReturn Code: {return_code}\n\n")
                self.protect_output_textbox.configure(state="disabled")


# Manifest_Operation_Function
        elif self.apk_function_dropdown.get() == "MANIFEST OPERATIONS":

            self.manifest_operation_run_btn.configure(fg_color="#0E8849")

            if self.manifest_operation_option_dropdown.get() == "DECODE":
                self.manifest_operation_output_textbox.insert("end", f"Extracting AndroidManifest.xml ...\n\nI: [Extract] Accessing APK File ...\nI: [Extract] Getting AndroidManifest.xml ...\nI: [Extract] Extracting to Destination ...\nI: [Fetch] Getting Extracted File ...\nI: [Decode] Decoding Data ...\nI: [Save] Copying Decoded File to Destination ...\n\nI: [Save] Saving Success! ...\n\nDone ...")
                self.extract_manifest()
                self.convert_xml_to_axml()

                self.manifest_operation_output_textbox.configure(state="normal")
                self.manifest_operation_run_btn.configure(fg_color=BTN_COLOR)

            else:
                self.manifest_operation_output_textbox.delete(1.0, "end")
                self.manifest_operation_output_textbox.insert("end", f"Encoding AndroidManifest.xml ...\n\nI: [Encode] Accessing Decoded AndroidManifest.xml File ...\nI: [Encode] Reading AndroidManifest.xml ...\nI: [Encode] Checking Changes Made ...\nI: [Encode] Encoding Data ...\nI: [Save] Copying Decoded File to Destination ...\n\nI: [Save] Saving Success! ...\n\nDone ...")
                self.convert_axml_to_xml()

                self.manifest_operation_output_textbox.configure(state="normal")
                self.manifest_operation_run_btn.configure(fg_color=BTN_COLOR)
                self.manifest_operation_output_textbox.configure(state="disabled")

            self.manifest_operation_sublime_btn.configure(state="normal", image=sublime_icon_enable)


# SignatureKiller_Function
        elif self.apk_function_dropdown.get() == "KILL SIGNATURE":

            self.signaturekill_run_btn.configure(fg_color="#0E8849")
            self.signaturekill_output_textbox.insert("end", f"Killing APK Signature ...\nInput: {apk_file}\nAPKSignatureKillerEx Working on ...\n")
            apk_path = self.apk_entry.get()

            try:
                with zipfile.ZipFile(apk_path, 'r') as zip_ref:

                    script_dir = os.path.dirname(os.path.abspath(__file__))

                    apkeditor_jar_filepath = "java_Packages\\APKEditor.jar"
                    apkeditor_jar_filepath_ = os.path.join(script_dir, apkeditor_jar_filepath)

                    java_command = f"java -jar {apkeditor_jar_filepath_} info -v -package -signatures-base64 -i {apk_path}"
                    output = subprocess.check_output(java_command, shell=True, text=True)

                    for line in output.split('\n'):
                        if 'package=' in line:
                            package_phrase = line.split('"')[1]

                    for line in output.split('\n'):
                        if 'Base64:' in line:
                            base64_phrase = line.split()[-1]

                    if self.signaturekill_option_dropdown.get() == "ADD ORIGIN APK":
                        self.find_and_replace()
                        self.add_origin_apk_to_signature_killer()
                        self.extract_signature_killer_zip()
                        self.replace_placeholder(package_phrase, base64_phrase)
                        self.copy_to_destination()
                        self.delete_temp()

                        self.signaturekill_output_textbox.configure(state="normal")
                        self.signaturekill_run_btn.configure(fg_color=BTN_COLOR)
                        self.signaturekill_output_textbox.insert("end", f"\nI: [SignatureKill] Getting Signature Data ...\nI: [SignatureKill] Getting Package Name ...\nI: [SignatureKill] Extracting Zip ...\nI: [SignatureKill] Find KillerApplication.smali ...\nI: [SignatureKill] Replacing Data ...\nI: [SignatureKill] Copying Content to Destination ...\n\nI: [SignatureKill] Copying Success! ...\n\nDone ...")
                        self.signaturekill_output_textbox.configure(state="disabled")
                
                    else:
                        self.find_and_replace()
                        self.extract_signature_killer_zip()
                        self.replace_placeholder(package_phrase, base64_phrase)
                        self.copy_to_destination()
                        self.delete_temp()

                        self.signaturekill_output_textbox.configure(state="normal")
                        self.signaturekill_run_btn.configure(fg_color=BTN_COLOR)
                        self.signaturekill_output_textbox.insert("end", f"\nI: [SignatureKill] Getting Signature Data ...\nI: [SignatureKill] Getting Package Name ...\nI: [SignatureKill] Extracting Zip ...\nI: [SignatureKill] Find KillerApplication.smali ...\nI: [SignatureKill] Replacing Data ...\nI: [SignatureKill] Copying Content to Destination ...\n\nI: [SignatureKill] Copying Success! ...\n\nDone ...")
                        self.signaturekill_output_textbox.configure(state="disabled")
                   
            except FileNotFoundError:
                print("APK file not found.")

        self.apk_function_dropdown.configure(state="normal")
        self.apk_function_confirm_btn.configure(state="normal")
        self.apk_function_reset_btn.configure(state='disabled', fg_color=BTN_COLOR)



    def count_apks_in_bundle(self, bundle_filename):
        count = 0
        with zipfile.ZipFile(bundle_filename, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith('.apk'):
                    count += 1
        return count
    


    def extract_signature_killer_zip(self):
       with zipfile.ZipFile('Java_Packages\\APKSignatureKillerEx.jar', 'r') as zip_ref:
           zip_ref.extractall('Temporary\\Killer')



    def replace_placeholder(self, package_phrase, signature_phrase):
       smali_file_path = os.path.join('Temporary', 'Killer', 'smali_classesx', 'bin', 'mt', 'signature', 'KillerApplication.smali')
       with open(smali_file_path, 'r') as file:
           data = file.read()

       replaced_data = data.replace('### PACKAGE ###', package_phrase).replace('### SIGNATURE ###', signature_phrase)

       with open(smali_file_path, 'w') as file:
          file.write(replaced_data)



    def copy_to_destination(self):
       apk_path_ = self.apk_entry.get()
       folder_path = os.path.splitext(apk_path_)[0]

       lib_folder_path = os.path.join(folder_path, 'lib')
       if not os.path.exists(lib_folder_path):
           os.makedirs(lib_folder_path)

       script_dir = os.path.dirname(os.path.abspath(__file__))

       apkeditor_jar_filepath = "java_Packages\\APKEditor.jar"
       apkeditor_jar_filepath_ = os.path.join(script_dir, apkeditor_jar_filepath)

       java_command = f"java -jar {apkeditor_jar_filepath_} info -v -dex -i {apk_path_}"
       output = subprocess.check_output(java_command, shell=True, text=True)

       dex_file_names = re.findall(r'Name="([^"]+)"', output)
       if dex_file_names:
          last_dex_file = dex_file_names[-1]
       else:
          last_dex_file = ""

       just_classes = last_dex_file.split('.')[0]

       if last_dex_file == "classes.dex":
          new_smali_folder_name = "smali_classes2"
       else:
          dex_number = int(just_classes[7:])
          new_dex_number = dex_number + 1
          new_smali_folder_name = f"smali_classes{new_dex_number}"

       shutil.copytree(os.path.join('Temporary', 'Killer', 'smali_classesx'), os.path.join(folder_path, new_smali_folder_name))
       
       lib_dir = os.path.join(folder_path, 'lib/arm64-v8a')
       os.makedirs(lib_dir, exist_ok=True)
       shutil.copy(os.path.join('Temporary', 'Killer', 'lib/arm64-v8a/libSignatureKiller.so'), lib_dir)

       lib_dir = os.path.join(folder_path, 'lib/armeabi-v7a')
       os.makedirs(lib_dir, exist_ok=True)
       shutil.copy(os.path.join('Temporary', 'Killer', 'lib/armeabi-v7a/libSignatureKiller.so'), lib_dir)



    def extract_manifest(self):
       apk = self.apk_entry.get()
       output_ = os.path.dirname(apk)
       output__ = os.path.basename(apk)
       output___ = os.path.splitext(output__)[0]
       output_dir = os.path.join(output_, "AM_"+output___)
       os.makedirs(output_dir, exist_ok=True)

       with zipfile.ZipFile(apk, 'r') as apk_zip:
           apk_zip.extract("AndroidManifest.xml", output_dir)

       extracted_manifest_path = os.path.join(output_dir, "AndroidManifest.xml")
       new_manifest_path = os.path.join(output_dir, "AndroidManifest_original.xml")
       os.rename(extracted_manifest_path, new_manifest_path)

       return new_manifest_path
    


    def convert_xml_to_axml(self):
       apk = self.apk_entry.get()
       output_ = os.path.dirname(apk)
       output__ = os.path.basename(apk)
       output___ = os.path.splitext(output__)[0]
       output_dir = os.path.join(output_, "AM_"+output___)

       input_path = output_dir+"\\"+"AndroidManifest_original.xml"
       output_path = output_dir+"\\"+"AndroidManifest-Decoded.xml"
       script_dir = os.path.dirname(os.path.abspath(__file__))

       sigtool_jar_filepath = "java_Packages\\Xml2Axml.jar"
       sigtool_jar_filepath_ = os.path.join(script_dir, sigtool_jar_filepath)
       java_command = f"java -jar {sigtool_jar_filepath_} d {input_path} {output_path}"
       subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



    def convert_axml_to_xml(self):
       apk = self.apk_entry.get()
       output_ = os.path.dirname(apk)
       output__ = os.path.basename(apk)
       output___ = os.path.splitext(output__)[0]
       output_dir = os.path.join(output_, "AM_"+output___)

       input_path = output_dir+"\\"+"AndroidManifest-Decoded.xml"
       output_path = output_dir+"\\"+"AndroidManifest.xml"
       script_dir = os.path.dirname(os.path.abspath(__file__))

       sigtool_jar_filepath = "java_Packages\\Xml2Axml.jar"
       sigtool_jar_filepath_ = os.path.join(script_dir, sigtool_jar_filepath)
       java_command = f"java -jar {sigtool_jar_filepath_} e {input_path} {output_path}"
       subprocess.run(java_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



    def add_origin_apk_to_signature_killer(self):
       source_apk_path = self.apk_entry.get()
       destination_folder = os.path.splitext(source_apk_path)[0]

       signature_killer_folder = os.path.join('Temporary', 'SignatureKiller')
       os.makedirs(signature_killer_folder, exist_ok=True)

       origin_apk_path = os.path.join(signature_killer_folder, "origin.apk")
       shutil.copy(source_apk_path, origin_apk_path)

       if "SignatureKiller" in signature_killer_folder:
          destination_folder_ = destination_folder+"\\"+"assets"
          shutil.copytree(signature_killer_folder, os.path.join(destination_folder_, "SignatureKiller"))



    def find_and_replace(self):
       apk_path_ = self.apk_entry.get()
       root_folder = os.path.splitext(apk_path_)[0]
       search_text = ".super Landroid/app/Application;"
       replace_text = ".super Lbin/mt/signature/KillerApplication;"
       replacement_done = False
       for folder, _, files in os.walk(root_folder):
            if replacement_done:
                break
            if "smali" in folder and not folder.endswith("smali_classesx"):
                for file in files:
                    if file.endswith(".smali"):
                        file_path = os.path.join(folder, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    if search_text in content:
                        updated_content = re.sub(re.escape(search_text), replace_text, content)
                        with open(file_path, 'w') as f:
                            f.write(updated_content)
                        self.signaturekill_output_textbox.configure(state="normal")
                        self.signaturekill_output_textbox.insert("end", f"\nKilling APK Signature ...\nPatched {file_path}\n")
                        self.signaturekill_output_textbox.configure(state="disabled")
                        replacement_done = True
                        break



    def delete_temp(self):
       temp_path = os.path.join("Temporary\\Killer")
       signature_path = os.path.join("Temporary\\SignatureKiller")
       bin_path =  os.path.join("Temporary\\bin")

       if os.path.exists(temp_path):
           shutil.rmtree(temp_path)

       if os.path.exists(signature_path):
           shutil.rmtree(signature_path)

       if os.path.exists(bin_path):
           shutil.rmtree(bin_path)



    def encode_apk_signature(self):
        decoded_bytes = base64.b64decode(unique_signature)
        decoded_string = decoded_bytes.decode('utf-8')
        webbrowser.open(decoded_string)
       


    def open_sublime(self):
        try:
            if self.apk_function_dropdown.get() == "DECOMPILE APK":
                apk = self.apk_entry.get()
                base_folder = os.path.dirname(apk)
                target_ = os.path.basename(apk)
                target_folder = os.path.splitext(target_)[0]
                path_to_target_folder = os.path.join(base_folder, target_folder)

                subprocess.Popen(["C:\\Program Files\\Sublime Text\\sublime_text.exe", path_to_target_folder])

            elif self.apk_function_dropdown.get() == "MANIFEST OPERATIONS":
                apk = self.apk_entry.get()
                output_ = os.path.dirname(apk)
                output__ = os.path.basename(apk)
                output___ = os.path.splitext(output__)[0]
                output_dir = os.path.join(output_, "AM_"+output___)
                target_file_path = os.path.join(output_dir, "AndroidManifest-Decoded.xml")

                subprocess.Popen(["C:\\Program Files\\Sublime Text\\sublime_text.exe", target_file_path])

            elif self.apk_function_dropdown.get() == "ARSC OPERATIONS":
                apk_filename = self.apk_entry.get()
                output_ = os.path.dirname(apk_filename)
                file_name = os.path.basename(apk_filename)
                output_dir = output_+"\\"+"ARSC_"+os.path.splitext(file_name)[0]
                dump_dir = output_dir+"\\"+"res.xml"+"\\"

                subprocess.Popen(["C:\\Program Files\\Sublime Text\\sublime_text.exe", dump_dir])

        except:
            messagebox.showerror("Couldn't load the File/Folder", ">> Make sure 'Sublime Text' installed in default location ('C:/Program Files/Sublime Text') on your PC\n>> Check the existence of target File/Folder")



    def open_arsceditor(self):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        arsce_filename = "java_Packages\\ArscEditor-GUI.jar"
        arsce_jar_file = os.path.join(script_dir, arsce_filename)

        command = f"java -jar {arsce_jar_file}"

        subprocess.Popen(command)



    def get_dex_file_list(self):

        apk_file_ = self.apk_entry.get()
        output_ = os.path.dirname(self.apk_entry.get())
        file_name = os.path.basename(apk_file_)
        output_dir = output_+"\\"+"DexDump_"+os.path.splitext(file_name)[0]
        os.makedirs(output_dir, exist_ok=True)

        dex_file_list = []

        with zipfile.ZipFile(apk_file_, 'r') as apk_zip:
           apk_file_list = apk_zip.namelist()
           for file in apk_file_list:
               if file.endswith('.dex'):
                 apk_zip.extract(file, output_dir)
                 dex_file_list.append(file)

        self.dex2smali_dex_name_entry.configure(values=dex_file_list)



    def get_smali_folder_list(self):

        apk_file_ = self.apk_entry.get()
        output_ = os.path.dirname(self.apk_entry.get())
        file_name = os.path.basename(apk_file_)
        output_dir = output_+"\\"+"DexDump_"+os.path.splitext(file_name)[0]+"\\"+"DexDump"

        smali_dir_list = []
        try:
            for folder_name in os.listdir(output_dir):
                folder_path = os.path.join(output_dir, folder_name)
                if os.path.isdir(folder_path) and folder_name.startswith("smali"):
                  smali_dir_list.append(folder_name)
        except:
            self.smali2dex_output_textbox.insert("end", f"Smali Folder not Found in Target Directory")

        self.smali2dex_smali_name_entry.configure(values=smali_dir_list)



    def reset_selected_funtion(self):
       
       self.apk_function_dropdown.configure(state='normal')
       self.apk_function_dropdown.set('VERIFY SIGNATURE')
       self.apk_function_confirm_btn.configure(state='normal')
       self.apk_function_reset_btn.configure(state='disabled', fg_color=BTN_COLOR)
       self.apk_picker_btn.configure(state="normal")



    def replace_file_in_apk(self):

        apk_file = self.apk_entry.get()
        replacement_files = self.replace_content_entry.get().split()
        replacement_files__ = os.path.basename(self.replace_content_entry.get())
        formatted_paths = "\n".join(replacement_files)
        try:
            with zipfile.ZipFile(apk_file, 'r') as original_apk:
                output = io.BytesIO()
                with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as modified_apk:
                    for item in original_apk.infolist():
                        if item.filename not in [os.path.basename(file) for file in replacement_files]:
                            modified_apk.writestr(item, original_apk.read(item.filename))
                        else:
                            for replacement_file in replacement_files:
                                if os.path.basename(replacement_file) == item.filename:
                                    modified_apk.writestr(item.filename, open(replacement_file, 'rb').read())
                                    break
                out_dir_mod = os.path.dirname(apk_file)
                out_dir_mod_apk = os.path.splitext(apk_file)[0] + "_replaced.apk"
                output_apk_path = os.path.join(out_dir_mod, out_dir_mod_apk)
                with open(output_apk_path, 'wb') as f:
                    f.write(output.getvalue())
            for replacement_file in replacement_files:
                self.replace_output_textbox.insert("end", f"\nReplaced Files:\n{replacement_files__}\n\nReplaced With:\n{formatted_paths}\n")
                self.replace_output_textbox.insert("end", f"\nOutput APK: {output_apk_path}")
                self.replace_output_textbox.configure(state="disabled")
                self.apk_function_dropdown.configure(state="normal")
                self.apk_function_confirm_btn.configure(state="normal", fg_color=BTN_COLOR)

        except Exception as e:
            print(f"Error occurred: {e}")



    def copy_content(self):
        content = self.apk_detail_output_textbox.get("1.0", "end-1c")
        print(content)



    def explore_apk(self):

        try:
            if self.apk_entry.get().endswith('.apkm') or self.apk_entry.get().endswith('.apks') or self.apk_entry.get().endswith('.zip') or self.apk_entry.get().endswith('.xapk'):
                url_app = f"https://play.google.com/store/apps/details?id={packID}&hl=en_US"
                webbrowser.open(url_app)
            else:
                url_app = f"https://play.google.com/store/apps/details?id={packID_}&hl=en_US"
                webbrowser.open(url_app)

        except:
            messagebox.showerror("Unable to Process your Request", ">> Couldn't get APK information")
                    
        
        
    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    apktool = APKToolGUI()
    apktool.run()