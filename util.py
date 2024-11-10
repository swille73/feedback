'''
Script containing utility functions
'''

_versionen = {
    # Auslieferung der Versionen
    # 06.05.2024
    '24.1.24121.606': '2024.1',
    # 03.06.2024
    '24.1.24155.423': '2024.1-1',
    # 02.07.2024
    '24.1.24179.845': '2024.1-2',
    # 22.07.2024
    '24.1.24201.408': '2024.1-3',
    # 02.09.2024
    '24.1.24242.576': '2024.1-4',
    # 01.10.2024
    '24.1.24274.682': '2024.1-5',
    # 21.10.2024
    '24.2.24275.452': '2024.2',
    # 27.10.2024 - Hotfix
    '24.2.24303.929': '2024.2-0a',
}


def get_version(version: str) -> str:
    '''
        Liefert die gewünschte Version zurück ansonsten die übergebene Version.
    '''
    return _versionen.get(version, "2023.2")
