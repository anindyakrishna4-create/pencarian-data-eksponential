# File: app.py (Revisi Final & Stabil - Gabungan Kode Algoritma)

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

# List global untuk menyimpan riwayat langkah
HISTORY = []

# =================================================================
# --- FUNGSI ALGORITMA EXPONENTIAL SEARCH (DIGABUNGKAN KE SINI) ---
# =================================================================

def _binary_search(arr, low, high, target):
    """Sub-rutin Binary Search yang disesuaikan untuk mencatat langkah."""
    global HISTORY
    found_index = -1
    
    HISTORY.append({
        'array': arr[:], 'target': target, 'low': low, 'high': high, 'mid': -1, 
        'status': 'Binary Start',
        'action': f'PHASE 2: Memulai Binary Search dalam rentang [{low} - {high}].'
    })

    while low <= high:
        mid = (low + high) // 2
        
        HISTORY.append({
            'array': arr[:], 'target': target, 'low': low, 'high': high, 'mid': mid,
            'status': 'Binary Mengecek',
            'action': f'Binary Search: Mengecek Indeks Tengah (mid={mid}). Nilai: {arr[mid]}.'
        })
        
        if arr[mid] == target:
            found_index = mid
            HISTORY.append({
                'array': arr[:], 'target': target, 'low': low, 'high': high, 'mid': mid,
                'status': 'Ditemukan',
                'action': f'Nilai {target} DITEMUKAN pada Indeks {mid}!'
            })
            return found_index
            
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    HISTORY.append({
        'array': arr[:], 'target': target, 'low': low, 'high': high, 'mid': -1,
        'status': 'Binary Gagal',
        'action': f'Binary Search selesai. Target {target} tidak ditemukan dalam rentang ini.'
    })
    return -1


def exponential_search(data_list, target):
    """Fungsi utama Exponential Search (Phase 1: Bounding, Phase 2: Binary Search)."""
    global HISTORY
    HISTORY = []
    
    arr = sorted(data_list[:]) 
    n = len(arr)
    
    if n == 0:
        HISTORY.append({'array': arr[:], 'target': target, 'status': 'Selesai', 'action': 'Array kosong.'})
        return -1, HISTORY

    HISTORY.append({'array': arr[:], 'target': target, 'status': 'Mulai', 'action': f'Memulai Exponential Search untuk {target}.'})

    if arr[0] == target:
        HISTORY.append({'array': arr[:], 'target': target, 'i': 0, 'status': 'Ditemukan', 'action': f'Nilai {target} DITEMUKAN pada Indeks 0.'})
        return 0, HISTORY

    # --- PHASE 1: Mencari Batasan (Bounding) ---
    i = 1 
    
    while i < n and arr[i] <= target:
        HISTORY.append({
            'array': arr[:], 'target': target, 'i': i, 'status': 'Melompat Eksponensial',
            'action': f'PHASE 1: Mengecek Indeks {i} (Nilai: {arr[i]}).'
        })
        i *= 2
    
    bound = min(i, n - 1)
    low = i // 2
    
    HISTORY.append({
        'array': arr[:], 'target': target, 'i': i, 'low': low, 'high': bound,
        'status': 'Batasan Ditemukan',
        'action': f'PHASE 1 Selesai. Rentang Binary Search: [{low} - {bound}].'
    })

    # --- PHASE 2: Binary Search ---
    found_index = _binary_search(arr, low, bound, target)
    
    if found_index == -1:
        HISTORY.append({'array': arr[:], 'target': target, 'status': 'Selesai', 'action': 'Pencarian Selesai. Target tidak ditemukan.'})
        
    return found_index, HISTORY
    
# =================================================================
# --- KONFIGURASI DAN STREAMLIT APP ---
# =================================================================

st.set_page_config(
    page_title="Virtual Lab: Exponential Search",
    layout="wide"
)

st.title("🚀 Virtual Lab: Exponential Search Interaktif")
st.markdown("### Visualisasi Algoritma Pencarian Eksponensial (Efektif untuk data sangat besar)")

st.sidebar.header("Konfigurasi Data dan Target")

default_data = "2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192" 
input_data_str = st.sidebar.text_input(
    "Masukkan data terurut (pisahkan dengan koma):", 
    default_data
)
target_value_str = st.sidebar.text_input("Masukkan Nilai Target yang Dicari:", "256")
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    if not data_list:
        st.error("Masukkan setidaknya satu angka untuk array.")
        st.stop()
    target_value = int(target_value_str.strip())
    initial_data_sorted = sorted(list(data_list))
except ValueError:
    st.error("Pastikan semua input data dan target adalah angka (integer) yang dipisahkan oleh koma.")
    st.stop()

# --- Penjelasan Pewarnaan (Kode Heksadesimal DIHAPUS) ---
st.markdown("""
#### Pewarnaan Bar:
* **Fase 1 (Lompatan):**
    * **Hijau:** Indeks **Lompatan (i)** yang sedang dicek.
    * **Kuning:** Array yang **sudah diperiksa** dalam lompatan eksponensial.
* **Fase 2 (Binary Search):**
    * **Biru:** Rentang **Pencarian Aktif** (rentang Binary Search).
    * **Orange:** Indeks **Tengah (mid)** yang sedang dicek.
* **Ungu:** Indeks di mana nilai **ditemukan**.
""")

st.write(f"**Array Terurut (Prasyarat):** {initial_data_sorted}")
st.write(f"**Nilai Target:** **{target_value}**")

# --- Fungsi Plot Matplotlib (Menggunakan Kode Warna Internal) ---
def plot_array(arr, state, found_index, max_val):
    fig, ax = plt.subplots(figsize=(12, 4))
    n = len(arr)
    x_pos = np.arange(n)
    
    colors = ['#CC0000'] * n # Merah: Default / Dibuang
    status = state['status']
    
    if status in ('Melompat Eksponensial', 'Batasan Ditemukan'):
        i = state['i']
        # Kuning (#F1C232): Area yang sudah diperiksa
        for k in range(min(i, n)):
            colors[k] = '#F1C232'
            
        # Hijau (#6AA84F): Indeks Lompatan (i)
        if i < n: colors[i // 2] = '#6AA84F' 
        if i < n: colors[min(i, n-1)] = '#6AA84F' # Tanda batas atas lompatan

    elif status.startswith('Binary'):
        low = state.get('low', -1)
        high = state.get('high', -1)
        mid = state.get('mid', -1)
        
        # Biru (#4A86E8): Rentang Pencarian Aktif
        if low != -1 and high != -1 and low <= high:
            for k in range(low, high + 1):
                 colors[k] = '#4A86E8'
                 
        # Orange (#FF9900): Mid
        if status == 'Binary Mengecek' and mid != -1:
            colors[mid] = '#FF9900'

    # Ungu (#8E44AD): Ditemukan
    if found_index != -1:
        colors[found_index] = '#8E44AD'
        
    ax.bar(x_pos, arr, color=colors)
    
    for k, height in enumerate(arr):
        ax.text(x_pos[k], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'I: {k}' for k in range(n)], rotation=0) 
    ax.set_ylabel('Nilai')
    ax.set_title(f"Pencarian Nilai: {target}", fontsize=14)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Exponential Search"):
    
    found_index, history = exponential_search(list(data_list), target_value)
    max_data_value = max(initial_data_sorted) if initial_data_sorted else 10 
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    final_found_index = -1
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        status = state['status']
        action = state['action']

        if status == 'Ditemukan':
            final_found_index = state.get('i') if 'i' in state else state.get('mid')
        
        fig_mpl = plot_array(current_array, state, final_found_index, max_data_value)

        with vis_placeholder.container():
            st.pyplot(fig_mpl, clear_figure=True)
        
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Array (Index & Nilai)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            if status == 'Ditemukan':
                st.success(f"**Langkah ke-{step}** | **Status:** {status}")
            elif status.endswith('Selesai') or status.endswith('Gagal'):
                st.error(f"**Langkah ke-{step}** | **Status:** {status}")
            else:
                 st.info(f"**Langkah ke-{step+1}** | **Status:** {status}")
            st.caption(action)

        time.sleep(speed)

    # --- Hasil Akhir Final ---
    st.markdown("---")
    if final_found_index != -1:
        st.balloons()
        st.success(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** DITEMUKAN pada Indeks **{final_found_index}**.")
    else:
        st.error(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** TIDAK DITEMUKAN dalam array.")
    
    st.info(f"Algoritma Exponential Search selesai dalam **{len(history)-1}** langkah visualisasi.")
