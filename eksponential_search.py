# File: exponential_search.py (Logika Algoritma)

# List global untuk menyimpan riwayat langkah
HISTORY = []

def _binary_search(arr, low, high, target, phase_start_step):
    """
    Sub-rutin Binary Search yang disesuaikan untuk mencatat langkah.
    """
    found_index = -1
    
    # Catat status awal Binary Search
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'low': low, 
        'high': high,
        'mid': -1, 
        'status': 'Binary Start',
        'action': f'PHASE 2: Memulai Binary Search dalam rentang [{low} - {high}]. (Langkah Awal: {phase_start_step})'
    })

    while low <= high:
        mid = (low + high) // 2
        
        # Catat langkah pengecekan Binary Search
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'low': low, 
            'high': high,
            'mid': mid,
            'status': 'Binary Mengecek',
            'action': f'Binary Search: Mengecek Indeks Tengah (mid={mid}). Nilai: {arr[mid]}.'
        })
        
        if arr[mid] == target:
            found_index = mid
            # Catat langkah Ditemukan
            HISTORY.append({
                'array': arr[:],
                'target': target,
                'low': low, 
                'high': high,
                'mid': mid,
                'status': 'Ditemukan',
                'action': f'Nilai {target} DITEMUKAN pada Indeks {mid}!'
            })
            return found_index
            
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    # Jika Binary Search selesai tanpa menemukan
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'low': low, 
        'high': high,
        'mid': -1,
        'status': 'Binary Gagal',
        'action': f'Binary Search selesai. Target {target} tidak ditemukan dalam rentang ini.'
    })
    return -1


def exponential_search(data_list, target):
    """
    Fungsi utama Exponential Search (Phase 1: Bounding, Phase 2: Binary Search).
    """
    global HISTORY
    HISTORY = []
    
    # Prasyarat: Array harus terurut!
    arr = sorted(data_list[:]) 
    n = len(arr)
    
    # Kasus dasar: Jika array kosong
    if n == 0:
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'i': -1, 
            'bound': -1,
            'status': 'Selesai',
            'action': 'Array kosong. Pencarian selesai.'
        })
        return -1, HISTORY

    # Catat status awal
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'i': -1, 
        'bound': -1,
        'status': 'Mulai',
        'action': f'Memulai Exponential Search untuk {target}. Array harus TERURUT.'
    })

    # Kasus 1: Elemen pertama adalah target
    if arr[0] == target:
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'i': 0, 
            'bound': 0,
            'status': 'Ditemukan',
            'action': f'Nilai {target} DITEMUKAN pada Indeks 0.'
        })
        return 0, HISTORY

    # --- PHASE 1: Mencari Batasan (Bounding) ---
    i = 1 # Mulai dari indeks 1
    
    while i < n and arr[i] <= target:
        # Catat langkah lompatan eksponensial
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'i': i, 
            'bound': -1,
            'status': 'Melompat Eksponensial',
            'action': f'PHASE 1: Mengecek Indeks {i} (Nilai: {arr[i]}). Nilai masih <= target.'
        })
        
        # Lompatan eksponensial
        i *= 2
    
    # Tentukan batas atas Binary Search
    # Batas atas adalah nilai 'i' terakhir yang tidak melewati array, atau n-1
    bound = min(i, n - 1)
    
    # Batas bawah Binary Search adalah setengah dari 'i' terakhir
    low = i // 2
    
    # Catat akhir fase bounding
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'i': i, 
        'bound': bound,
        'low': low,
        'high': bound,
        'status': 'Batasan Ditemukan',
        'action': f'PHASE 1 Selesai. Target mungkin berada dalam rentang Binary Search: [{low} - {bound}].'
    })

    # --- PHASE 2: Binary Search ---
    
    found_index = _binary_search(arr, low, bound, target, len(HISTORY))
    
    # Catat status akhir (HANYA jika tidak ditemukan di Binary Search)
    if found_index == -1:
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'i': -1, 
            'bound': -1,
            'status': 'Selesai',
            'action': 'Pencarian Exponential Search Selesai. Target tidak ditemukan.'
        })
        
    return found_index, HISTORY
