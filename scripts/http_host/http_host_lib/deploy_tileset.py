from pathlib import Path

import requests


def deploy_tileset():
    need_nginx_sync = False

    for area in ['planet', 'monaco']:
        r = requests.get(f'https://assets.openfreemap.com/versions/deployed_tiles_{area}.txt')
        r.raise_for_status()
        remote_version = r.text.strip()
        print(f'  remote version for {area}: {remote_version}')

        local_version_file = Path(f'/data/ofm/config/deployed_tiles_{area}.txt')

        if not local_version_file.exists():
            local_version_start = None
        else:
            with open(local_version_file) as fp:
                local_version_start = fp.read()

        if not remote_version:
            print('  remote version not specified')
            if local_version_start is not None:
                local_version_file.unlink()
                need_nginx_sync = True
            continue

        mnt_file = Path(f'/mnt/ofm/{area}-{remote_version}/metadata.json')
        if not mnt_file.exists():
            print('  local version does not exist')
            if local_version_start is not None:
                local_version_file.unlink()
                need_nginx_sync = True
            continue

        if remote_version != local_version_start:
            with open(local_version_file, 'w') as fp:
                fp.write(remote_version)
            need_nginx_sync = True

    return need_nginx_sync
