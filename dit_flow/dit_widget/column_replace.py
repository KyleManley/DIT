import csv
import os
import shutil

from ..rill import rill


@rill.component
@rill.inport('TEMPFILE')
@rill.inport('TEMPMAP')
@rill.inport('DATAFILE')
@rill.inport('DATAMAP')
@rill.inport('FID')
@rill.inport('SID')
@rill.inport('DESTFILE')
@rill.inport('DESTMAP')
@rill.outport('DATAFILE_OUT')
@rill.outport('DATAMAP_OUT')
@rill.outport('FID_OUT')
@rill.outport('SID_OUT')
@rill.outport('DESTFILE_OUT')
@rill.outport('DESTMAP_OUT')
def column_replace(TEMPFILE, TEMPMAP, DATAFILE, DATAMAP, FID, SID, DESTFILE,
                   DESTMAP, DATAFILE_OUT, DATAMAP_OUT, FID_OUT, SID_OUT,
                   DESTFILE_OUT, DESTMAP_OUT):
    """Replaces modified columns within the input csv file after operation.
    TEMPFILE: name of temporary file generated by widget
    TEMPMAP: dictionary of {column name: column index} for the temporary file
    DATAFILE: name of input csv file
    DATAMAP: dictionary of {column name: column index} for the input file
    FID: number 1... that identifies the order of the current file
    SID: number 1... that identifies the order of the current step
    DESTFILE: name of output csv file
    DESTMAP: dictionary of {column name: column index} for the output file
    """
    # TODO: Add information-writing functionality, like a file to write statistics to
    # The initialization of this file needs to happen in read_file though

    # BUG: On the last step in the flow, this hangs endlessly. I don't know
    #   which port is the problem, or a good way to find out.
    for tempfile, tempmap, datafile, datamap, fid, sid, destfile, destmap in \
        zip(TEMPFILE.iter_contents(), TEMPMAP.iter_contents(),
            DATAFILE.iter_contents(), DATAMAP.iter_contents(),
            FID.iter_contents(), SID.iter_contents(),
            DESTFILE.iter_contents(), DESTMAP.iter_contents()):
        
        # while True:
        #     tempfileP = TEMPFILE.receive()
        #     if tempfileP is None:
        #         continue
        #     else:
        #         tempfileP = tempfileP.get_contents()
        #     tempmapP = TEMPMAP.receive()
        #     if tempmapP is None:
        #         continue
        #     else:
        #         tempmapP = tempmapP.get_contents()
        #     datafileP = DATAFILE.receive()
        #     if datafileP is None:
        #         continue
        #     else:
        #         datafileP = datafileP.get_contents()
        #     datamapP = DATAMAP.receive()
        #     if datamapP is None:
        #         continue
        #     else:
        #         datamapP = datamapP.get_contents()
        #     fidP = FID.receive()
        #     if fidP is None:
        #         continue
        #     else:
        #         fidP = fidP.get_contents()
        #     sidP = SID.receive()
        #     if sidP is None:
        #         continue
        #     else:
        #         sidP = sidP.get_contents()
        #     destfileP = DESTFILE.receive()
        #     if destfileP is None:
        #         continue
        #     else:
        #         destfileP = destfileP.get_contents()
        #     destmapP = DESTMAP.receive()
        #     if destmapP is None:
        #         continue
        #     else:
        #         destmapP = destmapP.get_contents()

        # DEBUG: Reached the next set of packets
        print('replace', fid, sid)
        # Map indices in the temp file to indices in the in and out files
        indices = {tempmap[name]: destmap[name] for name in tempmap}
        indices_in = {tempmap[name]: datamap[name] for name in tempmap}

        with open(tempfile, newline='') as _temp, \
             open('tempout', 'w', newline='') as _out, \
             open(destfile, newline='') as _dest, \
             open('tempin', 'w', newline='') as _in, \
             open(datafile, newline='') as _original:
            # Modifies both the in and out files at the same time
            # Meaning that we really don't need the distinction and it would be cleaner with only one input/output file

            new = csv.reader(_temp)
            existing = csv.reader(_dest)
            modified_out = csv.writer(_out)
            original = csv.reader(_original)
            modified_in = csv.writer(_in)

            # Headlines
            modified_out.writerow(next(existing))
            modified_in.writerow(next(original))
            # Copy data
            for nline, eline, oline in zip(new, existing, original):
                output_out = eline
                output_in = oline
                for from_, to_ in indices.items():
                    output_out[to_] = nline[from_]
                for from_, to_ in indices_in.items():
                    output_in[to_] = nline[from_]
                modified_out.writerow(output_out)
                modified_in.writerow(output_in)
        shutil.move('tempout', destfile)
        shutil.move('tempin', datafile)

        # DEBUG: Print statements let us know when the ports are sending data
        print('data out', datafile)
        DATAFILE_OUT.send(datafile)
        print('data map out', datamap)
        DATAMAP_OUT.send(datamap)
        print('fid', fid)
        FID_OUT.send(fid)
        print('sid', sid)
        SID_OUT.send(sid + 1)
        print('dest', destfile)
        DESTFILE_OUT.send(destfile)
        print('dest map', destmap)
        DESTMAP_OUT.send(destmap)