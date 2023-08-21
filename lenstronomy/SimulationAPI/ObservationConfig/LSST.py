"""Provisional LSST instrument and observational settings.

See Optics and Observation Conditions spreadsheet at
https://docs.google.com/spreadsheets/d/1pMUB_OOZWwXON2dd5oP8PekhCT5MBBZJO1HV7IMZg4Y/edit?usp=sharing
for list of
sources.
"""
import copy
import lenstronomy.Util.util as util

__all__ = ['LSST']

u_band_obs = {'exposure_time': 15.,
              'sky_brightness': 22.99,
              'magnitude_zero_point': 26.5,
              'num_exposures': 140,
              'seeing': 0.81,
              'psf_type': 'GAUSSIAN'}

g_band_obs = {'exposure_time': 15.,
              'sky_brightness': 22.26,
              'magnitude_zero_point': 28.30,
              'num_exposures': 200,
              'seeing': 0.77,
              'psf_type': 'GAUSSIAN'}

r_band_obs = {'exposure_time': 15.,
              'sky_brightness': 21.2,
              'magnitude_zero_point': 28.13,
              'num_exposures': 460,
              'seeing': 0.73,
              'psf_type': 'GAUSSIAN'}

i_band_obs = {'exposure_time': 15.,
              'sky_brightness': 20.48,
              'magnitude_zero_point': 27.79,
              'num_exposures': 460,
              'seeing': 0.71,
              'psf_type': 'GAUSSIAN'}

z_band_obs = {'exposure_time': 15.,
              'sky_brightness': 19.6,
              'magnitude_zero_point': 27.40,
              'num_exposures': 400,
              'seeing': 0.69,
              'psf_type': 'GAUSSIAN'}

y_band_obs = {'exposure_time': 15.,
              'sky_brightness': 18.61,
              'magnitude_zero_point': 26.58,
              'num_exposures': 400,
              'seeing': 0.68,
              'psf_type': 'GAUSSIAN'}
"""
:keyword exposure_time: exposure time per image (in seconds)
:keyword sky_brightness: sky brightness (in magnitude per square arcseconds in units of electrons)
:keyword magnitude_zero_point: magnitude in which 1 count (e-) per second per arcsecond square is registered
:keyword num_exposures: number of exposures that are combined (depends on coadd_years)
    when coadd_years = 10: num_exposures is baseline num of visits over 10 years (x2 since 2x15s exposures per visit)
:keyword seeing: Full-Width-at-Half-Maximum (FWHM) of PSF
:keyword psf_type: string, type of PSF ('GAUSSIAN' supported)
"""


class LSST(object):
    """Class contains LSST instrument and observation configurations."""

    def __init__(self, band='g', psf_type='GAUSSIAN', coadd_years=10):
        """

        :param band: string, 'u', 'g', 'r', 'i', 'z' or 'y' supported. Determines obs dictionary.
        :param psf_type: string, type of PSF ('GAUSSIAN' supported).
        :param coadd_years: int, number of years corresponding to num_exposures in obs dict. Currently supported: 1-10.
        """
        if band.isalpha():
            band = band.lower()
        if band == 'g':
            self.obs = copy.deepcopy(g_band_obs)
        elif band == 'r':
            self.obs = copy.deepcopy(r_band_obs)
        elif band == 'i':
            self.obs = copy.deepcopy(i_band_obs)
        elif band == 'u':
            self.obs = copy.deepcopy(u_band_obs)
        elif band == 'z':
            self.obs = copy.deepcopy(z_band_obs)
        elif band == 'y':
            self.obs = copy.deepcopy(y_band_obs)
        else:
            raise ValueError("band %s not supported! Choose 'u', 'g', 'r', 'i', 'z' or 'y'." % band)

        if psf_type != 'GAUSSIAN':
            raise ValueError("psf_type %s not supported!" % psf_type)

        if coadd_years > 10 or coadd_years < 1:
            raise ValueError(" %s coadd_years not supported! Choose an integer between 1 and 10." % coadd_years)
        elif coadd_years != 10:
            self.obs['num_exposures'] = coadd_years*self.obs['num_exposures']//10

        self.camera = {'read_noise': 10,  # will be <10
                       'pixel_scale': 0.2,
                       'ccd_gain': 2.3,
                       }
        """:keyword read_noise: std of noise generated by read-out (in units of
        electrons) :keyword pixel_scale: scale (in arcseconds) of pixels :keyword
        ccd_gain: electrons/ADU (analog-to-digital unit)."""

    def kwargs_single_band(self):
        """

        :return: merged kwargs from camera and obs dicts
        """
        kwargs = util.merge_dicts(self.camera, self.obs)
        return kwargs
