import { Namer } from '@parcel/plugin';
import path from 'path';

export default new Namer({
  name({ bundle }) {
    if (!bundle.needsStableName) {
      let filePath = bundle.getMainEntry().filePath;
      return path.basename(filePath);
    }

    // Allow the next namer to handle this bundle.
    return null;
  }
});
