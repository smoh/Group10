# Data

* Use `download_Malo.sh` for Malo et al. 2013 catalog of moving group members
* `wget http://waps.cfa.harvard.edu/MIST/data/tarballs_v1.0/MIST_v1.0_vvcrit0.4_UBVRIplus.tar.gz` to get MIST isochrones and extract.

* candi_galexmatch.csv: all galex matches for candidate members within 2 arcsec from MAST GALEX catalog
* candi_phot_galex.csv: row-by-row match of deduplicated galex match to candi_phot and candi
* candi_phot_xray: row-by-row match of 2RXS X-ray source to candi_phot and candi

## "Field" stars with good parallax and photometry

```sql
select
  sub.designation, sub.parallax, sub.parallax_error,
  sub.bp_rp, sub.phot_bp_mean_mag, sub.phot_rp_mean_mag, sub.phot_g_mean_mag, sub.phot_variable_flag,
  ps.obj_id as ps_obj_id, ps.g_mean_psf_mag, ps.g_mean_psf_mag_error,
    ps.r_mean_psf_mag, ps.r_mean_psf_mag_error,
    ps.i_mean_psf_mag, ps.i_mean_psf_mag_error,
    ps.z_mean_psf_mag, ps.z_mean_psf_mag_error,
    ps.y_mean_psf_mag, ps.y_mean_psf_mag_error,
  tmass.j_m, tmass.j_msigcom,
  tmass.h_m, tmass.h_msigcom,
  tmass.ks_m, tmass.ks_msigcom,
  allwise.w1mpro, allwise.w1mpro_error,
  allwise.w2mpro, allwise.w2mpro_error,
  allwise.w3mpro, allwise.w3mpro_error,
  allwise.w4mpro, allwise.w4mpro_error
from (
  select * from gaiadr2.gaia_source
  where
      parallax_over_error>50
      and parallax>10
      -- emprical filtering of good bp, rp colors
      and ( (phot_bp_rp_excess_factor > 1+0.015*power(bp_rp,2))
          and (phot_bp_rp_excess_factor < 1.3+0.06*power(bp_rp,2)) )
          ) sub
-- panstarrs
left join gaiadr2.panstarrs1_best_neighbour
  on gaiadr2.panstarrs1_best_neighbour.source_id=sub.source_id
left join gaiadr2.panstarrs1_original_valid as ps
  on ps.obj_id = gaiadr2.panstarrs1_best_neighbour.original_ext_source_id
-- allwise
LEFT JOIN gaiadr2.allwise_best_neighbour
  on gaiadr2.allwise_best_neighbour.source_id=sub.source_id
LEFT JOIN gaiadr1.allwise_original_valid as allwise
  on allwise.allwise_oid = gaiadr2.allwise_best_neighbour.allwise_oid
-- tmass
LEFT JOIN gaiadr2.tmass_best_neighbour on
  gaiadr2.tmass_best_neighbour.source_id=sub.source_id
LEFT JOIN gaiadr1.tmass_original_valid tmass
  on tmass.tmass_oid = gaiadr2.tmass_best_neighbour.tmass_oid
```


## GALEX batch crossmatch

Guide: https://archive.stsci.edu/prepds/gcat/gcat_casjobs.html

```sql
select
  nb.objid, nb.distance as dstArcMin,p.ra,p.dec,
  p.band,p.glon,p.glat,p.nuv_mag,
  p.nuv_magerr,p.fuv_mag, p.fuv_magerr, p.e_bv,
  pe.nexptime,pe.fexptime,pe.mpstype as survey
from mydb.test_galex as s
left join PhotoObjAll as galex

from fgetnearbyobjeq(116.58073,42.66339, 5/*arcmins*/) as nb,
photoextract as pe,
photoobjall as p
where nb.objid=p.objid
and p.photoextractid=pe.photoextractid
and pe.nexptime > 3000 /*some threshold in seconds*/
and pe.mpstype='MIS' /* only MIS survey */
order by dstArcMin        
```
