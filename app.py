from flask import Flask, request, jsonify
from flask_cors import CORS# DELETE IN PRODUCTION?
import reedsolo

# Initialize Flask application
app = Flask(__name__)
CORS(app)# DELETE IN PRODUCTION?
# Endpoint to process a bit string
@app.route('/qr-reed-solomon', methods=['POST'])
def qr_reed_solomon():
    # Get the bit string from the request JSON data
    data = request.get_json()
    bit_string = data.get('bit_string')

    if bit_string is None:
        return jsonify({'error': 'Bit string is required in the request'}), 400


    def binary_string_to_bytes(binary_string):
        # Convert binary string to integer
        value = int(binary_string, 2)
        # Determine the number of bytes needed for the integer (ceil division by 8)
        num_bytes = (len(binary_string) + 7) // 8
        # Convert integer to bytes
        byte_data = value.to_bytes(num_bytes, byteorder='big')
        return byte_data

    def bytes_to_binary_string(byte_array):
        binary_string = ""
        for byte in byte_array:
            # Convert each byte to its binary representation (8 bits)
            # Use '{:08b}'.format(byte) to ensure each byte is represented as 8 bits
            binary_string += '{:08b}'.format(byte)
        return binary_string

    data = binary_string_to_bytes(bit_string)
    # Initialize the Reed-Solomon encoder with the required parameters
    rs = reedsolo.RSCodec(10)  # 10 ECC bytes
    # Encode the data
    ecc_encoded = rs.encode(data)

    bits_ecc = bytes_to_binary_string(ecc_encoded)

    # Return the processed bit string in the response
    return jsonify({'bits_ecc': bits_ecc})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)