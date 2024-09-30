# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:18:08 2021

@author: Erica Nocerino and Fabio Menna
"""

# Place the script in C:\Users\USERNAME\AppData\Local\Agisoft\Metashape Pro\scripts

import Metashape

def detect_underwater_testfield_targets():
    chunk = Metashape.app.document.chunk
    
    chunk.detectMarkers(Metashape.TargetType.CircularTarget14bit, tolerance=90, filter_mask=True, inverted=True,noparity=False, maximum_residual=500, minimum_size=0, minimum_dist=5)
    UW_testfield_target_names = list(range(1,384))
    Metashape_target_names = [  24,  20,  12,  18,  10,   6,  30,  17,   9,   5,  29,   3,  27,
                                23,  15,  16,   8,   4,  28,   2,  26,  22,  14,   1,  25,  21,
                                13,  19,  11,   7,  31,  32,  71,  55,  67,  51,  43,  90,  65,
                                49,  41,  88,  37,  84,  77,  61,  64,  48,  40,  87,  36,  83,
                                76,  60,  34,  81,  74,  58,  70,  54,  46,  93,  63,  47,  39,
                                86,  35,  82,  75,  59,  33,  80,  73,  57,  69,  53,  45,  92,
                                79,  72,  56,  68,  52,  44,  91,  66,  50,  42,  89,  38,  85,
                                78,  62,  96,  95,  94,  97, 151, 124, 110, 195, 102, 188, 173,
                               146, 106, 122, 108, 193, 100, 186, 171, 144, 182, 167, 140, 160,
                               133, 119, 204, 121, 107, 192,  99, 185, 170, 143, 181, 166, 139,
                               159, 132, 118, 203, 179, 164, 137, 157, 130, 116, 201, 154, 127,
                               113, 198, 105, 191, 176, 149, 150,  98, 184, 169, 142, 180, 165,
                               138, 158, 131, 117, 202, 178, 163, 136, 156, 129, 115, 200, 153,
                               126, 112, 197, 104, 190, 175, 148, 177, 162, 135, 155, 128, 114,
                               199, 152, 125, 111, 196, 103, 189, 174, 147, 123, 109, 194, 101,
                               187, 172, 145, 183, 168, 141, 161, 134, 120, 205, 206, 207, 217,
                               216, 214, 211, 215, 213, 210, 212, 209, 208, 218, 219, 220, 341,
                               322, 282, 336, 317, 277, 306, 264, 240, 371, 298, 314, 273, 303,
                               260, 236, 368, 296, 253, 229, 362, 351, 332, 292, 247, 246, 245,
                               335, 316, 276, 305, 263, 239, 370, 255, 313, 272, 302, 259, 235,
                               367, 295, 252, 228, 361, 350, 331, 291, 311, 270, 300, 257, 233,
                               365, 275, 250, 226, 359, 348, 329, 289, 223, 356, 345, 326, 286,
                               340, 321, 281, 310, 268, 244, 375, 294, 262, 238, 297, 231, 312,
                               271, 301, 258, 234, 366, 251, 227, 360, 349, 330, 290, 269, 299,
                               256, 232, 364, 249, 225, 358, 347, 328, 288, 222, 355, 344, 325,
                               285, 339, 320, 280, 309, 267, 243, 374, 334, 248, 224, 357, 327,
                               221, 343, 284, 319, 308, 242, 353, 323, 337, 278, 265, 372, 274,
                               261, 369, 230, 352, 293, 380, 379, 381, 387]

    for current_marker in chunk.markers:
        try:
            ms_number = int(current_marker.label.split()[1])
            UW_number = Metashape_target_names.index(ms_number)
            print(ms_number,UW_number)
            current_marker.label = str( UW_testfield_target_names[UW_number])
        except:
            print('Marker not available:', current_marker.label)           
    

Metashape.app.addMenuItem("Custom/Detect UW_testfield  targets", detect_underwater_testfield_targets)